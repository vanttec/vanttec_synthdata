
#* 10/09/2024 ,_,
#* Create blender file configurated for synth data from an STL file

'''
This Python script can be run on its own to create the blender file configurated for synth data as:
    blender --background --python PreparedBlendScene.py -- --stl_path "/path/to/file.stl" --object_name MyObject --num_frames [optional] --img_pixels_x [optional] --img_pixels_y [optional]
    or
    blenderproc run PreparedBlendScene.py -- --stl_path "/path/to/file.stl" --object_name MyObject --num_frames [optional] --img_pixels_x [optional] --img_pixels_y [optional]

The created scene will be saved as follows:
    ~/object_name/
        object_name.blend


or run the classes in a separate script with:
    import PreparedBlendScene.py

    def main():
        blender_creation = BlenderSetup(args)
        blender_creation.run()
'''

import bpy
import os
import math
import sys

def parse_args(): # When blender runs in background it is not compatible with argparse, instead sys is used
    '''Parses arguments when run as a standalone Blender script'''
    args = sys.argv[sys.argv.index("--") + 1:]
    args_dict = {}
    for i in range(0, len(args), 2):
        key = args[i].lstrip("--")
        value = args[i + 1]
        args_dict[key] = value
    return args_dict

class CameraSetup:
    def __init__(self, radius, location, num_frames, object_name):
        self.radius = radius
        self.location = location
        self.num_frames = num_frames
        self.num_frames = num_frames
        self.object_name = object_name

    def create_path(self):
        '''Create a Bézier circle with a fixed radius'''
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='CURVE')
        bpy.ops.object.delete()
        
        curve_data = bpy.data.curves.new(name='BezierCircle', type='CURVE')
        curve_data.dimensions = '3D'
        curve_obj = bpy.data.objects.new('BezierCircle', curve_data)
        bpy.context.collection.objects.link(curve_obj)
        
        spline = curve_data.splines.new(type='BEZIER')
        spline.bezier_points.add(8 - 1)
        RADIUS_FACTORS = [1, 1.2, 1.4, 1.6]  # Adjustment factors for each quadrant
        
        # Position the points on the circle, this will create an uneven circle to improve the randomization of the images
        for i in range(8):
            angle = 2 * math.pi * i / 8
            quadrant = i // 2
            current_radius = self.radius * RADIUS_FACTORS[quadrant]
            x, y = current_radius * math.cos(angle), current_radius * math.sin(angle)
            spline.bezier_points[i].co = (x, y, 0)
            spline.bezier_points[i].handle_left_type = 'AUTO'
            spline.bezier_points[i].handle_right_type = 'AUTO'
        
        spline.use_cyclic_u = True  # Close the path
        curve_obj.location = self.location
        return curve_obj

    def create_target(self, location):
        '''Create an invisible cube'''
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        cube = bpy.context.object
        cube.name = 'InvisibleCube'
        cube.hide_viewport = True
        cube.hide_render = True
        cube.hide_set(True)
        return cube

    def apply_track_constraint(self, camera, target_obj):
        '''Apply the 'Track To' constraint to make the camera follow the object'''
        # Ensure the camera is not hidden before applying constraints
        camera.hide_viewport = False
        camera.hide_render = False
        
        # Set the camera as active and apply the constraint
        bpy.context.view_layer.objects.active = camera
        if target_obj:
            bpy.ops.object.constraint_add(type='TRACK_TO')
            camera.constraints["Track To"].target = target_obj
            camera.constraints["Track To"].up_axis = 'UP_Y'
            camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'

    def apply_followpath(self, camera, bezier_circle):
        '''Apply the constraint so that the camera follows a path'''
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        constraint = camera.constraints["Follow Path"]
        constraint.target = bezier_circle
        constraint.use_curve_follow = True
        constraint.forward_axis = 'FORWARD_Y'
        constraint.up_axis = 'UP_Z'

    def set_camera_keyframes(self, camera):
        '''Configure keyframes for camera animation'''
        start_frame = 1
        end_frame = self.num_frames  # Access the instance attribute self.num_frames
        bpy.context.scene.frame_start = start_frame
        bpy.context.scene.frame_end = end_frame
        
        camera.constraints["Follow Path"].offset = 0
        camera.constraints["Follow Path"].keyframe_insert(data_path="offset", frame=start_frame)
        camera.constraints["Follow Path"].offset = self.num_frames
        camera.constraints["Follow Path"].keyframe_insert(data_path="offset", frame=end_frame)

    def create_camera(self):
        '''Create a camera'''
        bpy.ops.object.camera_add(location=(0.1, 0, 0))
        camera = bpy.context.object
        camera.rotation_euler = (0, 0, 0)
        return camera
        
    def run(self):
        '''Execute the camera configuration'''
        camera = self.create_camera()
        bezier_circle = self.create_path()
        target = self.create_target(location=(0, 0, 0))
        self.apply_track_constraint(camera, target)
        self.apply_followpath(camera, bezier_circle)
        self.set_camera_keyframes(camera)

class ObjectSetup:
    def __init__(self, obj_name, stl_path, num_frames):
        self.obj_name = obj_name
        self.stl_path = stl_path
        self.num_frames = num_frames

    def scale_object(self, obj, target_size):
        '''Scale an object to a target size'''
        dimensions = obj.dimensions
        max_dimension = max(dimensions)
        scale_factor = target_size / max_dimension
        obj.scale = (scale_factor, scale_factor, scale_factor)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(scale=True)

    def apply_black_shader(self, obj):
        '''Create and assign a black material to the object'''
        material = bpy.data.materials.new(name="BlackMaterial")
        material.diffuse_color = (0, 0, 0, 1)
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1)
        
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

    def animate_object_movement(self, obj, num_frames, move_distance, speed):
        obj.keyframe_insert(data_path="location", frame=1)
        
        for frame in range(2, num_frames + 1):
            if frame % (2 * speed) <= speed:
                obj.location.x = (frame % (2 * speed)) * (move_distance / speed) - (move_distance / 2)
            else:
                obj.location.x = (move_distance / 2) - (frame % (2 * speed) - speed) * (move_distance / speed)
            obj.keyframe_insert(data_path="location", frame=frame)
            
    def import_stl(self, stl_path, obj_name, num_frames):
        '''Import an STL file at the default position 0,0,0,0'''
        if not os.path.exists(stl_path):
            raise FileNotFoundError(f"The STL file was not found at: {stl_path}")
        bpy.ops.import_mesh.stl(filepath=stl_path) 
        obj = bpy.context.selected_objects[0]
        obj.name = obj_name
        return obj  # Ensure the object is returned

    def run(self):
        '''Execute the object configuration'''
        obj = self.import_stl(self.stl_path, self.obj_name, self.num_frames)  # Get the imported object
        self.scale_object(obj, target_size=10.0)  # Now 'obj' is a valid object
        self.apply_black_shader(obj)
        self.animate_object_movement(obj, self.num_frames, move_distance=5, speed=1)

class BlenderSetup():
    def __init__(self, args):
        self.stl_path = args['stl_path']
        self.object_name = args['object_name']
        self.num_frames = int(args.get("num_frames", 100))
        self.img_pixels_x = int(args.get("img_pixels_x", 512))
        self.img_pixels_y = int(args.get("img_pixels_y", 512))

    def add_freestyle_lines(self):
        '''Add Freestyle lines to the render'''
        bpy.context.scene.render.use_freestyle = True
        freestyle = bpy.context.view_layer.freestyle_settings
        
        if freestyle.linesets:
            freestyle.linesets.remove(freestyle.linesets[0])
        
        line_set = freestyle.linesets.new(name="WhiteLineSet")
        line_style = bpy.data.linestyles.new(name="WhiteLineStyle")
        line_set.linestyle = line_style
        line_style.color = (1.0, 1.0, 1.0)
    
    def define_image_size(self):
        '''Configure image size parameters'''
        bpy.context.scene.render.resolution_x = self.img_pixels_x
        bpy.context.scene.render.resolution_y = self.img_pixels_y
        bpy.context.scene.render.film_transparent = True

    def define_output(self):
        '''Create an output directory to save the .blend file.'''
        output_dir = os.path.join(os.path.expanduser("~"), self.object_name) # user's home directory/object_name
        os.makedirs(output_dir, exist_ok=True)  # Create the folder if it does not exist
        return output_dir
        
    def run(self):
        '''Complete execution of the configuration in Blender'''
        bpy.ops.wm.read_factory_settings(use_empty=True)
        
        # Object configuration
        object_setup = ObjectSetup(self.object_name, self.stl_path, self.num_frames)
        object_setup.run()

        # Camera configuration
        camera_setup = CameraSetup(radius=30, location=(0, 0, 0), num_frames=self.num_frames, object_name=self.object_name)
        camera_setup.run()

        # Add Freestyle and set image size
        self.add_freestyle_lines()
        self.define_image_size()

        # Save .blend file
        output_dir = self.define_output()
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(output_dir, f"{self.object_name}.blend"))
    
def main():
    args = parse_args()
    blender_creation = BlenderSetup(parse_args())
    blender_creation.run()

if __name__ == '__main__':
    main()