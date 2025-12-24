import open3d as o3d
import gc
import time
import os
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
        part_filename = f"FullCampusPart{i}.ply"
        inlier_filename = f"IIITB_InlierCloud_Part{i}.ply"
        
        # Load point cloud
        start = time.perf_counter()
        ptCloud = o3d.io.read_point_cloud(part_filename)
        end = time.perf_counter()
        load_time = end - start
        load_size = os.path.getsize(part_filename) / 1024  # in KB
        load_num_points = len(ptCloud.points)
        
        # Log to CSV after loading
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([part_filename, 'Load', load_time, load_size, load_num_points, 'N/A'])
        
        print(f"Loaded point cloud for {part_filename}: {load_num_points}")
        print(f"Time taken to load {part_filename}: {load_time:.4f} seconds")
        
        # Parameters
        noNeighbours = 10  # No of neighbours
        sdRatio = 1.5      # Std deviation ratio

        # Statistical filtering
        start = time.perf_counter()
        inlierCloud, outlierCloud = ptCloud.remove_statistical_outlier(
            nb_neighbors=noNeighbours, std_ratio=sdRatio
        )
        end = time.perf_counter()
        filter_time = end - start
        filter_num_points = len(inlierCloud.points)
        
        # Calculate % reduction in points
        reduction_percent = 100 * (1 - filter_num_points / load_num_points)

        # Log to CSV after filtering
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([part_filename, 'Filter', filter_time, 'N/A', filter_num_points, reduction_percent])

        print(f"Inlier cloud for {part_filename}: {filter_num_points}")
        print(f"Time taken for statistical filtering on {part_filename}: {filter_time:.4f} seconds")
        print(f"Percentage reduction in points: {reduction_percent:.2f}%")

        # Saving results
        start = time.perf_counter()
        o3d.io.write_point_cloud(inlier_filename, inlierCloud)
        end = time.perf_counter()
        save_time = end - start
        save_size_inlier = os.path.getsize(inlier_filename) / 1024  # in KB

        # Log to CSV after saving
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([part_filename, 'Save Inlier', save_time, save_size_inlier, filter_num_points, 'N/A'])

        print(f"Time taken to save clouds for {part_filename}: {save_time:.4f} seconds")
        print(f"Size of saved inlier cloud: {save_size_inlier:.2f} KB")

        gc.collect()  # Force garbage collection to free memory
    except Exception as e:
        print(f"An error occurred while processing Part{i}: {e}")
        gc.collect()  # Ensure memory is freed even on error