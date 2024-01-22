import laspy
from datetime import datetime, timedelta
import os

folder_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_TrainingSet\Train_Dataset\ThreePlots'

files = os.listdir(folder_path)

total_num_points = 0
for file in files:    
    if file.endswith(".laz"):
        file_path = os.path.join(folder_path, file)
        las_file = laspy.read(file_path)
        # Access the point format to get information about the attributes
        # point_format = las_file.point_format        
        num_points = las_file.header.point_count
        print("{}: {}".format(file, num_points))
        total_num_points = total_num_points + num_points
     
print(total_num_points)

                
    


   
