# Installation Instructions for NVIDIA OpticalFlow SDK for Python 
To use the NVIDIA OpticalFlow SDK in Python you need to use the Opencv wrapper for the C++.

Requements:
 - CUDA Toolkit 10.2 or higher
 - CMake 3.14 or later.
 - GCC/G++ 5.1 or newer
 - Opencv 4 or higher

## Cuda toolkit installation
The installation instruction for Cuda can be found here: https://developer.nvidia.com/cuda-downloads

Below are the specific instructions for Ubuntu 20.04Lts local:

```
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
$ sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
$ wget https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda-repo-ubuntu2004-11-4-local_11.4.0-470.42.01-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu2004-11-4-local_11.4.0-470.42.01-1_amd64.deb
$ sudo apt-key add /var/cuda-repo-ubuntu2004-11-4-local/7fa2af80.pub
$ sudo apt-get update
$ sudo apt-get -y install cuda
```

## CMake
CMake can be installed directly using the command below.
```
$ sudo apt-get install cmake
```

## GCC and G++
```
$ sudo apt install gcc g++
```

## OpenCV
OpenCV can be with `pip` package manage in Python3. However, it will not have the modules for cuda and optical flow. These modules are found in the extra modules repository `opencv_contrib`. Therefore, opencv will have to be built with extra modules from `opencv_contrib` in order to use the optical flow sdk wrapper in opencv.

To build from source:

### Step 1: get opencv and opencv_contrib from github
Getting opencv repository

```
$ git clone https://github.com/opencv/opencv.git
```

Getting opencv_contrib repository

```
$ git clone https://github.com/opencv/opencv_contrib.git
```

### Step 2: Create build directory in opencv
```
$ cd opencv;
$ mkdir build
```

### Step 3: Run Make with extra modules
```
$ cmake -DOPENCV_EXTRA_MODULES_PATH=<opencv_contrib>/modules <opencv_source_directory>
$ make -j5
```

### Step 4: Install 
```
$ sudo make install
```

Installation is done. In Python these two lines should work and show the installed version of OpenCV.
```python
import cv2 as cv
print(cv.__version__)
```