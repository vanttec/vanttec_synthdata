#!/bin/bash

# Settings used for accessing X11 server and thus getting graphics within the container
DOCKER_GRAPHICS_ARGS="--env DISPLAY --env QT_X11_NO_MITSHM=1 --volume=/tmp/.X11-unix:/tmp/.X11-unix:rw --device=/dev/dri:/dev/dri"

xhost +

docker run -it -d\
    $DOCKER_GRAPHICS_ARGS \
    --name uuv_synth \
    --gpus all \
    --privileged \
    -v "/dev/bus/usb/:/dev/bus/usb" \
    -v "${PWD%/*/*}:/ws/vanttec_synth" \
    uuv_synth \
    /bin/bash