import laspy
from datetime import datetime, timedelta


file_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_TrainingSet\Train_Dataset\Train_Dataset_Classified\Sample_data_nonselected\test\labelled\L23FCNSW796_segmented_raw_Label_0000000.laz'
las_file = laspy.read(file_path)
   
# Access the point format to get information about the attributes
point_format = las_file.point_format
print("Point Format:", point_format)
num_points = las_file.header.point_count
# Access the names of the fields (attribute names)
field_names = list(point_format.dimension_names)

print("Field Names:", field_names)

# # Iterate over the points and print each field value
# for point in las_file.points:
#     for field_name in field_names:
#         value = getattr(point, field_name)
#         print(f"{field_name}: {value}")
min_x, min_y, min_z = las_file.header.min
max_x, max_y, max_z = las_file.header.max

# Calculate center point coordinates
center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
center_z = (min_z + max_z) / 2

# Create dictionaries for boundary and center coordinates
boundary_dict = {
    "min_x": min_x, "min_y": min_y, "min_z": min_z,
    "max_x": max_x, "max_y": max_y, "max_z": max_z
}

center_dict = {
    "center_x": center_x, "center_y": center_y, "center_z": center_z
}




# Access specific attributes
x = las_file.x  # x-coordinate
y = las_file.y  # y-coordinate
z = las_file.z  # z-coordinate
print(len(x), len(y), len(z))
intensity = las_file.intensity
classification = las_file.classification
# range = las_file.range
# ring = las_file.ring
# label = las_file.label
# gps_time = las_file.gpstime


# Print the first few values of each attribute for demonstration
print("X:", len(x))
print("Y:", y[:10])
print("Z:", z[:10])
# print("Intensity:", intensity[:10])
# print("Classification:", classification[:10])
# print("Label:", label[:10])
# Close LAS file
las_file.close()