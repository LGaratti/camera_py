import numpy as np
import cv2
import os
import datetime
import pyrealsense2 as rs

def display_frames(depth_frames, color_frames, visualization_event):
    for idx, (depth_frame, color_frame) in enumerate(zip(depth_frames, color_frames)):
        if depth_frame is not None and color_frame is not None:
            
            # Convert frames to numpy arrays for visualization
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Depth manipulation
            desired_min_distance = 0
            desired_max_distance = 2500
            depth_image_clipped = np.clip(depth_image, desired_min_distance, desired_max_distance)
            depth_image_normalized = cv2.normalize(depth_image_clipped, None, 0, 255, cv2.NORM_MINMAX)
            depth_colormap = cv2.applyColorMap(depth_image_normalized.astype(np.uint8), cv2.COLORMAP_JET)

            # Combine two images for horizontal display
            depth_colormap_dim = depth_colormap.shape
            color_colormap_dim = color_image.shape
            if depth_colormap_dim != color_colormap_dim:
                resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                images = np.hstack((resized_color_image, depth_colormap))
            else:
                images = np.hstack((color_image, depth_colormap))

            window_name = f'RealSense {idx}'
            cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(window_name, images)
        else:
            print(f"Camera {idx}: No image data available to display.")
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        visualization_event.clear() 
                    
def save_frames(depth_frames, color_frames, intrinsics):
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pc = rs.pointcloud()
    
    for idx, (depth_frame, color_frame, camera_intrinsics) in enumerate(zip(depth_frames, color_frames, intrinsics)):
        if depth_frame is not None and color_frame is not None:
            try:
                # Creating save directories
                save_folder = os.path.join('media','save', current_time, str(idx))
                save_path = os.path.abspath(save_folder)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                # File paths
                depth_file = os.path.join(save_path, current_time + '_D.png')
                color_file = os.path.join(save_path, current_time + '_C.png')
                ply_file = os.path.join(save_path, current_time + '.ply')
                
                # Image processing
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                # Depth frame manipulation
                depth_image_clipped = np.clip(depth_image, 0, 2500)
                depth_image_normalized = cv2.normalize(depth_image_clipped, None, 0, 255, cv2.NORM_MINMAX)
                depth_colormap = cv2.applyColorMap(depth_image_normalized.astype(np.uint8), cv2.COLORMAP_JET)

                # Save images
                cv2.imwrite(depth_file, depth_colormap)
                cv2.imwrite(color_file, color_image)

                # Generate and save point cloud
                pc.map_to(color_frame)
                points = pc.calculate(depth_frame)
                v, t = points.get_vertices(), points.get_texture_coordinates()
                verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
                texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv

                # Filter points and save point cloud
                filtered_verts, filtered_texcoords = filter_points(verts, texcoords)
                save_ply(ply_file, filtered_verts, filtered_texcoords, color_image)
            except Exception as e:
                print(f"Error saving images for camera {idx}: {e}")
        else:
            print(f"Camera {idx}: No image data available to save.")

def filter_points(verts, texcoords, max_distance=4.0):
    # Calculate the Euclidean distance from the origin.
    distances = np.linalg.norm(verts, axis=1)
    # Create a mask for points within the maximum distance.
    mask = distances < max_distance
    # Apply mask to vertices and texture coordinates.
    filtered_verts = verts[mask]
    filtered_texcoords = texcoords[mask]
    return filtered_verts, filtered_texcoords

def save_ply(file_path, verts, texcoords, color_image):
    with open(file_path, "w") as ply_file:
        ply_file.write("ply\n")
        ply_file.write("format ascii 1.0\n")
        ply_file.write("element vertex %d\n" % len(verts))
        ply_file.write("property float x\n")
        ply_file.write("property float y\n")
        ply_file.write("property float z\n")
        ply_file.write("property uchar red\n")
        ply_file.write("property uchar green\n")
        ply_file.write("property uchar blue\n")
        ply_file.write("end_header\n")

        # Pre-processing of data
        verts = verts * [1, -1, -1]  # Flip y and z axis
        texcoords = texcoords * [color_image.shape[1], color_image.shape[0]]
        texcoords = texcoords.astype(np.int32)
        # Clip texcoords to be within image bounds
        texcoords = np.clip(texcoords, [0, 0], [color_image.shape[1] - 1, color_image.shape[0] - 1])
        # Get colors in a single NumPy operation
        colors = color_image[texcoords[:, 1], texcoords[:, 0]]
        # Combine information into a single array
        data = np.hstack([verts, colors])
        # Write all data at once
        np.savetxt(ply_file, data, fmt="%f %f %f %d %d %d")