import laspy
import textwrap
import os
import numpy as np

class HeightNormalization:
    """
    Sanity check: .laz data has been height normalised or not

    The raw .laz data is representing the terrain elevation of real world, so it can be started from positive or negative values.
    However, to do process the data properly it needs to be relocated on the o ground, so it is called 'height nomalizing, aka hnom'
    this script can check whether it is hight normailsed or non    
    """
    
    def __init__(self, parent_path):
        self.parent_path = parent_path
        self.hnomdir_name = 'Normalized_data'        
        self.odir_path = os.path.join(self.parent_path, self.hnomdir_name)
        
    def sanity_check(self):
        las_list = os.listdir(self.parent_path)
        to_be_hnom_data_list = []
        hnom_data_list = []
        for laz_file in las_list:
            if laz_file.endswith(".laz") or laz_file.endswith(".las"):
                laz_file_path = os.path.join(self.parent_path, laz_file)
                laz_file = laspy.read(laz_file_path)                
                z_scaled = laz_file.z  # ScaledArrayView
                height = np.array(z_scaled)
                if np.min(height) == 0:
                    to_be_hnom_data_list.append(laz_file_path)
                else:
                    hnom_data_list.append(laz_file_path)
        
        return [to_be_hnom_data_list, hnom_data_list]
                        
    def abstract(self):
            
            intro = f"""
            Sanity check: .laz data has been height normalised or not

            The raw .laz data is representing the terrain elevation of real world, so it can be started from positive or negative values.
            However, to do process the data properly it needs to be relocated on the o ground, so it is called 'height nomalizing, aka hnom'
            This readme file gives two lists that are containing the file paths depending on normalised status
             : normalised
             : non-normalised
             
             
             * non-normalised .laz or las file that we need to focus on
            
            The following is information:
            -------------------------------------------------------------------------------------------------------------------------------------
            """
            
            return intro
    
    def write_readme(self, hnom_check_list):
        # Specify the file path        
        txt_file_name = 'README.txt'
        readme_file_path = os.path.join(self.parent_path, txt_file_name)
        normalised_path_list = hnom_check_list[0]
        non_normalised_path_list = hnom_check_list[-1]

        # Open the file in write mode ('w')
        with open(readme_file_path, 'w') as f:
            abstract_text = textwrap.dedent(self.abstract()).strip()
            if abstract_text:
                f.write(abstract_text + "\n\n")

            # Write the list of strings
            f.write("- normalised_path_list:\n")
            for nomalized in normalised_path_list:
                if isinstance(nomalized, list):
                    # If the item is a list, write its elements
                    for subitem in nomalized:
                        f.write(str(subitem) + "\n")
                else:
                    # If the item is not a list, write it directly
                    f.write(str(nomalized) + "\n\n")
            f.write("\n\n")
            # Write the list of strings
            f.write("- non_normalised_path_list:\n")
            for non_nomalized in non_normalised_path_list:
                if isinstance(non_nomalized, list):
                    # If the item is a list, write its elements
                    for subitem in non_nomalized:
                        f.write(str(subitem) + "\n")
                else:
                    # If the item is not a list, write it directly
                    f.write(str(non_nomalized) + "\n")            

        
    def create_subdir(self):
        
        if not os.path.exists(self.odir_path):
            os.mkdir(self.odir_path)
            print("{} folder is created".format(self.hnomdir_name))
        else:
            print("{} folder is already there".format(self.hnomdir_name))
        
    def cmd_executor(self, lasheight_path, hnom_check_list):
        non_hnom_path_list = hnom_check_list[-1]
        self.create_subdir()
        for non_hnom_laz_file in non_hnom_path_list:
            cmd = lasheight_path + " -i " + non_hnom_laz_file + " -replace_z -classify_above 80 7 -keep_class 0 -odix _hnom -odir " + self.odir_path + " -olaz"
            os.system(cmd)
            print("{} is h-normalised".format(os.path.split(non_hnom_laz_file)[-1]))

        print("normalised is done")

def main():
    lasheight_path = r'C:\LAStools\bin\lasheight.exe'
    parent_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_PlayGroundSet\data_hnom'
    
    hnObj = HeightNormalization(parent_path)
    hnom_check_list = hnObj.sanity_check()
    hnObj.write_readme(hnom_check_list)
    hnObj.cmd_executor(lasheight_path, hnom_check_list)
                   
 
if __name__ == "__main__":
    main()