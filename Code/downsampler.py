import open3d as o3d
import time
import os
import gc
import csv

# CSV file header and setup
csv_file = 'processing_log.csv'
csv_header = ['Filename', 'Process', 'Time (s)', 'File Size (KB)', 'Number of Points', 'Percentage Reduction']

# Initialize CSV file if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

# Loop through Part1 to Part7
for i in range(1, 8):
    try:
        inlier_filename = f"IIITB_InlierCloud_Part{i}_B.ply"
        voxel_filename = f"IIITB_VoxelDSampledCloud_Part{i}_B.ply"
        
        # Load point cloud
        start = time.perf_counter()
        inlierCloud = o3d.io.read_point_cloud(inlier_filename)
        end = time.perf_counter()
        load_time = end - start
        load_size = os.path.getsize(inlier_filename) / 1024  # in KB
        load_num_points = len(inlierCloud.points)
        
        # Log to CSV after loading
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([inlier_filename, 'Load', load_time, load_size, load_num_points, 'N/A'])
        
        print(f"Loaded point cloud for {inlier_filename}: {load_num_points}")
        print(f"Time taken to load {inlier_filename}: {load_time:.4f} seconds")

        # Voxel downsampling
        start = time.perf_counter()
        VoxelDSampledCloud = inlierCloud.voxel_down_sample(voxel_size=0.008)
        end = time.perf_counter()
        downsample_time = end - start
        downsample_num_points = len(VoxelDSampledCloud.points)
        
        # Calculate % reduction in points after downsampling
        downsample_reduction_percent = 100 * (1 - downsample_num_points / load_num_points)

        # Log to CSV after downsampling
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([inlier_filename, 'Downsample', downsample_time, 'N/A', downsample_num_points, downsample_reduction_percent])

        print(f"Voxel downsampled cloud for {inlier_filename}: {downsample_num_points}")
        print(f"Time taken for voxel downsampling on {inlier_filename}: {downsample_time:.4f} seconds")
        print(f"Percentage reduction in points after downsampling: {downsample_reduction_percent:.2f}%")

        # Saving results
        start = time.perf_counter()
        o3d.io.write_point_cloud(voxel_filename, VoxelDSampledCloud)
        end = time.perf_counter()
        save_time = end - start
        save_size_voxel = os.path.getsize(voxel_filename) / 1024  # in KB

        # Log to CSV after saving
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([inlier_filename, 'Save Voxel', save_time, save_size_voxel, downsample_num_points, 'N/A'])

        print(f"Time taken to save clouds for {inlier_filename}: {save_time:.4f} seconds")
        print(f"Size of saved voxel cloud: {save_size_voxel:.2f} KB")

        gc.collect()  # Force garbage collection to free memory
    except Exception as e:
        print(f"An error occurred while processing Part{i}: {e}")
        gc.collect()  # Ensure memory is freed even on error
