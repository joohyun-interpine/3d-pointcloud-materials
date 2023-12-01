import laspy
from datetime import datetime, timedelta


file_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_PlayGroundSet\data_selection\tree62_dl.las'
las_file = laspy.read(file_path)
   
# Access the point format to get information about the attributes
point_format = las_file.point_format
print("Point Format:", point_format)

# Access the names of the fields (attribute names)
field_names = list(point_format.dimension_names)

print("Field Names:", field_names)

# # Iterate over the points and print each field value
# for point in las_file.points:
#     for field_name in field_names:
#         value = getattr(point, field_name)
#         print(f"{field_name}: {value}")
        
# Access specific attributes
x = las_file.x  # x-coordinate
y = las_file.y  # y-coordinate
z = las_file.z  # z-coordinate
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
