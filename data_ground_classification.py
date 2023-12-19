import laspy
import textwrap
import os
import numpy as np

class GroundClassification:
    
    def __init__(self, parent_path):
        self.parent_path = parent_path 
    
    def processes(self):
                
        # find 10th percentile points as candidates for ground points
        lasthin -i %WORK_DIR%\Temp\05_tiles_buffered\*.laz -set_classification 1 -step 0.25 -percentile 5 20 -classify_as 8 -odir %WORK_DIR%\Temp\06_tiles_thinned_01 -olaz -cores %CORES%
        lasthin -i %WORK_DIR%\Temp\06_tiles_thinned_01\*.laz -step 0.3333 -percentile 5 20 -classify_as 8 -odir %WORK_DIR%\Temp\06_tiles_thinned_02 -olaz -cores %CORES%
        lasthin -i %WORK_DIR%\Temp\06_tiles_thinned_02\*.laz -step 0.5 -percentile 5 20 -classify_as 8 -odir %WORK_DIR%\Temp\06_tiles_thinned_03 -olaz -cores %CORES%

        # classify 10th percentile points as lower ground
        lasground -i %WORK_DIR%\Temp\06_tiles_thinned_03\*.laz -ignore_class 1 -town -ultra_fine -ground_class 2 -odir %WORK_DIR%\Temp\07_tiles_ground_low -olaz -cores %CORES%

        # include points within a short distance of lower ground to make thick ground
        # this values in classify_between gives in general good results
        lasheight -i %WORK_DIR%\Temp\07_tiles_ground_low\*.laz -classify_between -0.05 0.17 6 -odir %WORK_DIR%\Temp\07_tiles_ground_thick -olaz -cores %CORES%

        # find median point to use as ground from thick ground

        lasthin -i %WORK_DIR%\Temp\07_tiles_ground_thick\*.laz -ignore_class 1 -step 0.5 -percentile 50 -classify_as 8 -odir %WORK_DIR%\Temp\07_tiles_ground_median -olaz -cores %CORES%

        # reclassify low ground which was in a temporary class
        lasclassify -i %WORK_DIR%\Temp\07_tiles_ground_median\*.laz -change_classification_from_to 6 2 -odir %WORK_DIR%\Temp\08_tiles_classified_ground -olaz -cores %CORES%
        
        
def main():
    lasheight_path = r'C:\LAStools\bin\lasheight.exe'
    parent_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_PlayGroundSet\data_hnom'
    
    gcObj = GroundClassification(parent_path)

                   
 
if __name__ == "__main__":
    main()