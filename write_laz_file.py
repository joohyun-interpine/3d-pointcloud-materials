import laspy

file_path = r'C:\Users\JooHyunAhn\Interpine\GitRepos\TreeTools\data\LIR184_FT_output\LIR184_segmented_raw.laz'
output_file_path = r'C:\Users\JooHyunAhn\Interpine\GitRepos\TreeTools\data\LIR184_FT_output\LIR184_segmented_no_label.laz'
las_file = laspy.read(file_path)

las_file = laspy.read(file_path)

# Access the point format to get information about the attributes
point_format = las_file.point_format
print("Point Format:", point_format)

# Access the names of the fields (attribute names)
field_names = list(point_format.dimension_names)
print("Field Names:", field_names)

# Create a list of field names excluding 'label'
fields_to_keep = [field_name for field_name in field_names if field_name != 'label']

# Create a new LAS file without the 'label' field
header = las_file.header
header.data_format_id = 1  # Update the data format ID as needed
header.point_format_id = 3  # Update the point format ID as needed
header.point_count = len(las_file.points)

out_las = laspy.LasData(header)
for field_name in fields_to_keep:
    setattr(out_las, field_name, getattr(las_file, field_name))

out_las.write(output_file_path)
print("New LAS file created:", output_file_path)


def create_delivery_folder_client():
    