# OpticalFlowVisual

### requirements
 - Python3
 - OpenCV
 - imutils
 - NVIDIA Optical Flow SDK*

Use ```pip install imutils``` to install imutils.

### Usage

Running the script with an input video file:
```
$ python nvof_visual.py 'path/to/input/video_file_name' 'grid_size' 'line_thickness' 'flow_scale'
```
 - `grid_size` represents the size of the distance between flow tracking points, default is 5.
 - `line_thickness` the thickness of the flow lines, default is 1.
 - `flow_scale` scale length of the flow lines, default is 1.

The output video file will be in output/video_file_name

When you run the script without the an input file,
```
$ python nvof_visual.py
```
it defaults to using the inbuilt webcam and save the processed video in output/cam.avi file.

For the RGB version:
```
$ python nvof_visual_rgb.py 'path/to/input/video_file_name' 'grid_size'
```
When the grid_size is not specified, the output will default to a 5x5 grid.

