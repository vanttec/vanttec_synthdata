<p align="center">
  <img src="docs/vanttec.png" width="320" height="180"/>
</p>

# VantTec's Synthetic Data Repository


This is the Vanttec's repository used for synthetic data generation used to feed image segmentation and object detection models. It runs with docker containers and a GPU.


```Shell
cd
git clone --recurse-submodules https://github.com/vanttec/vanttec_synthdata.git
```

Inside the /vanttec_uuv/dockerfiles/ directory you would two options to select: 
* ubuntu2204
* ubuntu2204_gpu

Each option contains a Dockerfile (image) and their respective create_container.bash, so please select the one that suits you the most and continue:

```Shell
cd ~/vanttec_uuv/dockerfiles/{selected_option}
docker build -t uuv_synth .
./create_container.bash
docker exec -it uuv_synth /bin/bash
```

**Was the GUI working and now isn't? Please use:**

```Shell
docker stop uuv_synthdata
docker rm uuv_synthdata
cd ~/vanttec_uuv/dockerfiles/{selected_option}./create_container.bash
docker exec -it uuv_synthdata /bin/bash
```