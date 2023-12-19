import numpy as np
import laspy
from datetime import datetime, timedelta

file_path = r'V:\FCNSW_Hovermap_2023\Train_Dataset - Copy\L23FCNSW688_segmented_raw.laz'
las_file = laspy.read(file_path)
# Load your 3D point cloud data (replace this with your actual data loading code)
# Assuming your point cloud data is stored in a variable called 'point_cloud'
# Each row of 'point_cloud' should represent a point with X, Y, Z coordinates.

# Example point cloud data
point_cloud = np.array([
    [1.0, -2.0, 3.0],
    [2.0, -1.0, 4.0],
    [3.0, -3.0, 5.0],
    # ... more points ...
])

# Find the lowest point on the slope
lowest_point = np.min(point_cloud[:, 2])  # Z coordinates

# Calculate the vertical shift based on the lowest point
vertical_shift = abs(lowest_point)

# Apply the vertical shift
point_cloud[:, 2] += vertical_shift



# # Access the point format to get information about the attributes
point_format = las_file.point_format
# # Access the names of the fields (attribute names)
field_names = list(point_format.dimension_names)

# Create a list of field names excluding 'label'
fields_to_keep = [field_name for field_name in field_names if field_name != 'label']

# Create a new LAS file without the 'label' field
header = las_file.header
header.data_format_id = 1  #  The new LAS file should be in a standard LAS format
header.point_format_id = 3  # The new LAS point format with X, Y, Z coordinates and intensity
header.point_count = len(las_file.points)

# Write a laz file with the given header which does not have 'label'
out_las = laspy.LasData(header)
for field_name in fields_to_keep:
    setattr(out_las, field_name, getattr(las_file, field_name))

out_las.write(new_laz_output_file_path)
