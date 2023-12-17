import os
import time
import pyrealsense2 as rs
import threading

# Event objects for thread synchronization
save_event = threading.Event()
info_event = threading.Event()
visualization_event = threading.Event()
exit_event = threading.Event()

current_fps = {}
fps_list = []

def initialize_cameras():
    context = rs.context()
    # Detect the number of connected cameras
    camera_count = context.query_devices().size()

    if camera_count == 0:
        print("No RealSense cameras found!")
        exit(0)
    print("Found ", camera_count , " Realsense")

    pipelines = []
    configs = []

    # Configure pipelines and configs for each detected camera
    for i in range(camera_count):
        pipeline = rs.pipeline(context)
        config = rs.config()
        config.enable_device(context.query_devices()[i].get_info(rs.camera_info.serial_number))
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipelines.append(pipeline)
        configs.append(config)

    return pipelines, configs

def get_intrinsics(pipeline):
    profile = pipeline.get_active_profile()
    video_profile = profile.get_stream(rs.stream.color)  # Assuming color stream intrinsics are needed
    intrinsics = video_profile.as_video_stream_profile().get_intrinsics()
    return intrinsics

def acquire_frames(pipelines):
    depth_frames = []
    color_frames = []

    for pipeline in pipelines:
        frames = pipeline.wait_for_frames()
        
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            depth_frames.append(None)
            color_frames.append(None)
        else:
            depth_frames.append(depth_frame)
            color_frames.append(color_frame)
                    
    return depth_frames, color_frames