import threading
import datetime
import cv2

from camera_utils import initialize_cameras, get_intrinsics, acquire_frames
from display_utils import display_frames, save_frames
from console_input import console_input, save_event, info_event, visualization_event, exit_event, fps_list

def main():
    # Create pipelines and configs for the number of detected cameras
    pipelines, configs = initialize_cameras()
    intrinsics = []
    # Start pipelines with their respective configs
    for pipeline, config in zip(pipelines, configs):
        pipeline.start(config)
        intrinsics.append(get_intrinsics(pipeline))
    # Start the console input thread
    input_thread = threading.Thread(target=console_input)
    input_thread.start()
    # TODO Thread for only acquire
    # TODO Thread for only save
    # TODO Thread for only info
    try:
        global current_fps, fps_list
        while not exit_event.is_set():
            start_time = datetime.datetime.now()
            depth_frames, color_frames = acquire_frames(pipelines) # TODO Thread for only acquire
            if depth_frames is not None and color_frames is not None:
                end_time = datetime.datetime.now()
                elapsed_time = (end_time - start_time).total_seconds()
                if elapsed_time > 0:
                    current_fps = 1.0 / elapsed_time  # Corrected here
                else:
                    current_fps = 0.0
                if visualization_event.is_set():
                    # TODO: Start a new thread for visualization
                    display_frames(depth_frames, color_frames, visualization_event)
                else:
                    cv2.destroyAllWindows()
                # Handle the saving of frames
                if save_event.is_set():
                    save_frames(depth_frames, color_frames, intrinsics) # TODO Thread for only save
                    save_event.clear()
                if info_event.is_set():
                    fps_list.append(current_fps)
                    print(f"Insert q to quit --- Cameras FPS: {current_fps:.2f}")
                if exit_event.is_set():
                    break
    finally:
        # Stop all pipelines
        for pipeline in pipelines:
            pipeline.stop()

if __name__ == "__main__":
    main()