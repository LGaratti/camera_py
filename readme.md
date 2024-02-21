# camera_py Camera Acquisition and Diagnostic Tool

## Description
This project is a tool designed for the acquisition, saving, and diagnostics of RealSense cameras. Initially tailored to work with multiple RealSense D435 cameras, due to my familiarity with these models, the goal is to extend compatibility to other cameras, including non-RGBD models, in the future. It offers functionalities for frame viewing and saving, as well as monitoring camera performance in terms of FPS.

## Features
- **Camera Detection and Initialization**: Automatically detects connected RealSense cameras and initializes them.
- **Frame Acquisition**: Simultaneously captures color and depth frames from all connected cameras.
- **Frame Display**: Real-time display of color and depth frames.
- **Frame and Point Cloud Saving**: Saves frames and point clouds in a specified format.
- **FPS Monitoring**: Calculates and displays real-time FPS, and provides an option to view average FPS.

## Prerequisites
- Python 3.x
- PyRealSense2 library
- OpenCV
- Numpy

## Installation
To install the necessary dependencies, run the following commands:
```
pip install pyrealsense2
pip install opencv-python
pip install numpy
```

## Acknowledgements
This project leverages the following open-source libraries:
- [RealSense SDK 2.0](https://github.com/IntelRealSense/librealsense): The core library for RealSense camera functionality.
- [OpenCV](https://github.com/opencv/opencv): Utilized for image processing and frame visualization.

## Project Structure
- `main.py`: The main script to run for starting the camera acquisition and processing pipeline.
- `camera_utils.py`: Contains functions for camera detection, initialization, and frame acquisition.
- `display_utils.py`: Manages the display and saving of color and depth frames, as well as point cloud generation.
- `console_input.py`: Handles user input from the console to control the application's behavior.

## Usage
To use this tool, please follow these steps:
1. Ensure all RealSense cameras are connected to your computer.
2. Execute the `main.py` script to initiate the program:
   ```
   python main.py
   ```
3. Utilize the on-screen prompts to save frames, display FPS information, or terminate the program.

### Commands
- `s`: Save the current frames from all cameras.
- `i`: Display the current FPS and compute the average FPS.
- `v`: Toggle the real-time visualization of depth and color frames.
- `q`: Exit the application.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.