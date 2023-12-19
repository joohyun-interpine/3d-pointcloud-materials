import laspy
import math
import pandas as pd
from tabulate import tabulate
import numpy as np
pd.set_option('display.max_colwidth', None) # this is just to check a dataframe easily

class StraightnessScore:
    def __init__(self, parent_path):
        self.parent_path = parent_path
     
    def read_csv(self, csv_file_path):
        df = pd.read_csv(csv_file_path, sep=',')
        
        return df

    # Function to calculate distance between two points
    def calculate_distance(self, x1, y1, x2, y2):
        
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def data_derivation(self, df):
        bottom_center_x = 0
        bottom_center_y = 0
        df['Relocate_X'] = df['Bin_X'] - df['Base_X']
        df['Relocate_Y'] = df['Bin_Y'] - df['Base_Y']
        df['Distance_From_Center'] = ((df['Relocate_X'] - bottom_center_x)**2 + (df['Relocate_Y'] - bottom_center_y)**2).apply(math.sqrt)
        
        df['Radius'] = df['MA_Diameter'] / 2
        
        return df

    def get_furthest_cylinders(self, df):
        
        df_sorted = df.sort_values(by='Height_Bin')        
        max_distance_index = df_sorted['Distance_From_Center'].idxmax()
        max_distance_row = df_sorted.loc[max_distance_index].to_frame().T
        
        bottom_cylinder_row = df.nsmallest(1, 'Height_Bin')
        top_cylinder_row = df.nlargest(1, 'Height_Bin')
        
        # Concatenate DataFrames with ignore_index set to False
        discovered_df = pd.concat([max_distance_row, bottom_cylinder_row, top_cylinder_row], ignore_index=False)
        discovered_sorted_df = discovered_df.sort_values(by='Height_Bin')
        
        bottom_xy_radius = tuple(discovered_sorted_df.iloc[0, df.columns.get_indexer(['Relocate_X', 'Relocate_Y', 'Radius'])])
        top_xy_radius = tuple(discovered_sorted_df.iloc[-1, df.columns.get_indexer(['Relocate_X', 'Relocate_Y', 'Radius'])])
        
        furthested_sorted_df = discovered_df.sort_values(by='Distance_From_Center')
        furthest_xy_radius = tuple(furthested_sorted_df.iloc[-1, df.columns.get_indexer(['Relocate_X', 'Relocate_Y', 'Radius'])])
        
        bottom_furthest_coor_radius = [bottom_xy_radius, furthest_xy_radius]
        bottom_top_furthest_coor_radius = [bottom_xy_radius, top_xy_radius, furthest_xy_radius]        
 
        return [discovered_sorted_df, bottom_furthest_coor_radius, bottom_top_furthest_coor_radius]


    def get_length_hypotenuse_xy(self, two_coordinates):        

        hypotenuse = self.calculate_distance(two_coordinates[0][0], two_coordinates[0][1], two_coordinates[1][0], two_coordinates[1][1])
        x_length = abs(two_coordinates[-1][0] - two_coordinates[0][0])
        y_length = abs(two_coordinates[-1][-1] - two_coordinates[0][-1])
        
        return hypotenuse, x_length, y_length    
        
    def get_theta(self, hypotenuse, x_length):
        y_length = math.sqrt(hypotenuse**2 - x_length**2)
        cosine_theta = x_length / hypotenuse
        theta_degree = math.degrees(math.acos(cosine_theta))
        
        sine_theta = y_length / hypotenuse
        sine_degree = math.degrees(math.acos(sine_theta))
        
        return [cosine_theta, theta_degree, sine_theta, sine_degree]
    
    def get_edge_coord(self, theta_cosine, top_cyl_coord, origin_coord):
        edge_x = theta_cosine * origin_coord[-1]        
        edge_y = math.sqrt((origin_coord[-1] ** 2) - (edge_x ** 2))
        
        if top_cyl_coord[0] < 0 and top_cyl_coord[1] >= 0:
            zone = 'zone 1'
            edge_coor = ((origin_coord[0] - edge_x), (origin_coord[1] + edge_y))            
        elif top_cyl_coord[0] >= 0 and top_cyl_coord[1] >= 0:
            zone = 'zone 2'
            edge_coor = ((origin_coord[0] + edge_x), (origin_coord[1] + edge_y))            
        elif top_cyl_coord[0] < 0 and top_cyl_coord[1] < 0:
            zone = 'zone 3'
            edge_coor = ((origin_coord[0] - edge_x), (origin_coord[1] - edge_y))            
        else:
            zone = 'zone 4'
            edge_coor = ((origin_coord[0] + edge_x), (origin_coord[1] - edge_y))            
        
        
        return [zone, edge_coor]
        
    def get_furthest_circumference_coordinates(self, cylinders_info, theta_phi_list):
        
        bottom_top_furthest_coordinates = cylinders_info[2]
        
        # bottom_cylider
        bottom_cyl_coord = bottom_top_furthest_coordinates[0]        
        
        # top_cylider
        top_cyl_coord = bottom_top_furthest_coordinates[1]
        furthest_cyl_coord = bottom_top_furthest_coordinates[2]
        
        # furthest_cylider
        theta_cosine = theta_phi_list[0]
        theta_degree = theta_phi_list[1]
        print("The degree from the center point from the bottom cylider to the center point of the top cylinder is {}".format(theta_degree))
        bottom_edge_coor = self.get_edge_coord(theta_cosine, top_cyl_coord, bottom_cyl_coord)
        top_edge_coor = self.get_edge_coord(theta_cosine, top_cyl_coord, top_cyl_coord)
        furthest_edge_coor = self.get_edge_coord(theta_cosine,  top_cyl_coord, furthest_cyl_coord)
        
        cylinders_info_height_sorted = cylinders_info[0].sort_values(by='Height_Bin')        
        
        cylinders_info_height_sorted.loc[cylinders_info_height_sorted.index[0], 'Zone'] = bottom_edge_coor[0]
        cylinders_info_height_sorted.loc[cylinders_info_height_sorted.index[0], 'Cylinder_Edge_X'] = bottom_edge_coor[1][0]
        cylinders_info_height_sorted.loc[cylinders_info_height_sorted.index[0], 'Cylinder_Edge_Y'] = bottom_edge_coor[1][1]
        
        cylinders_info_height_sorted.loc[cylinders_info_height_sorted.index[-1], 'Zone'] = top_edge_coor[0]
        cylinders_info_height_sorted.loc[cylinders_info_height_sorted.index[-1], 'Cylinder_Edge_X'] = top_edge_coor[1][0]
        cylinders_info_height_sorted.loc[cylinders_info_height_sorted.index[-1], 'Cylinder_Edge_Y'] = top_edge_coor[1][1]
        
        cylinders_info_distance_sorted = cylinders_info_height_sorted.sort_values(by='Distance_From_Center')
        
        cylinders_info_distance_sorted.loc[cylinders_info_distance_sorted.index[-1], 'Zone'] = furthest_edge_coor[0]
        cylinders_info_distance_sorted.loc[cylinders_info_distance_sorted.index[-1], 'Cylinder_Edge_X'] = furthest_edge_coor[1][0]
        cylinders_info_distance_sorted.loc[cylinders_info_distance_sorted.index[-1], 'Cylinder_Edge_Y'] = furthest_edge_coor[1][1]
        
        df = cylinders_info_distance_sorted
        
        return df

    def distances_add_from_edge(self, df):
        cylinders_info_height_sorted = df.sort_values(by='Height_Bin')
        bottom_cyl_edge_x = cylinders_info_height_sorted.iloc[0]['Cylinder_Edge_X']
        bottom_cyl_edge_y = cylinders_info_height_sorted.iloc[0]['Cylinder_Edge_Y']
        cylinders_info_height_sorted['Distance_From_CenterEdge'] = ((cylinders_info_height_sorted['Cylinder_Edge_X'] - bottom_cyl_edge_x)**2 + (cylinders_info_height_sorted['Cylinder_Edge_Y'] - bottom_cyl_edge_y)**2).apply(math.sqrt)
        
        return cylinders_info_height_sorted

    def point_on_line_at_height(self, start_coords, end_coords, target_height):
        """
            Using the theory of the parametric equation of a line.
            Refer to, (http://www.nabla.hr/PC-ParametricEqu1.htm)

        Args:
            start_coords (_type_): _description_
            end_coords (_type_): _description_
            target_height (_type_): _description_

        Returns:
            _type_: _description_
        """
        x1, y1, z1 = start_coords
        x2, y2, z2 = end_coords
        
        # Solve for t when z = target_height
        t = (target_height - z1) / (z2 - z1)

        # Calculate the coordinates of the point on the line
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        z = target_height
        
        return (x, y, z)    
    
    def get_final_furthest_coord(self, furthest_coord, parametric_coord_by_height, distance_length):
        """
        the direction vector of the line and scale it by the desired distance

        Args:
            furthest_coord (_type_): _description_
            parametric_coord_by_height (_type_): _description_
            distance_length (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Convert points to numpy arrays for easier vector operations
        a = np.array(parametric_coord_by_height)
        b = np.array(furthest_coord)

        # Calculate the direction vector
        direction_vector = b - a

        # Normalize the direction vector
        normalized_direction = direction_vector / np.linalg.norm(direction_vector)

        # Calculate the new point along the line at the desired distance
        new_point = a + distance_length * normalized_direction

        return tuple(new_point)
    
    def get_length_hypotenuse_3d_coord(self, df):
        # coord1 and coord2 are tuples or lists representing 3D coordinates (x, y, z)
        topx1, topy1, topz1 = df.iloc[-1]['Cylinder_Edge_X'], df.iloc[-1]['Cylinder_Edge_Y'], df.iloc[-1]['Height_Bin'] 
        bottomx1, bottomy1, bottomz1 = df.iloc[0]['Cylinder_Edge_X'], df.iloc[0]['Cylinder_Edge_Y'], df.iloc[0]['Height_Bin'] 
        
        cylinders_info_distance_sorted = df.sort_values(by='Distance_From_CenterEdge')
        furthesstx1, furthessty1, furthesstz1 = cylinders_info_distance_sorted.iloc[-1]['Cylinder_Edge_X'], cylinders_info_distance_sorted.iloc[-1]['Cylinder_Edge_Y'], cylinders_info_distance_sorted.iloc[-1]['Height_Bin'] 
        
        # About the top and bottom cylinders
        d3_hypotenuse_between_top_bottom = math.sqrt((topx1 - bottomx1)**2 + (topy1 - bottomy1)**2 + (topz1 - bottomz1)**2)
        length_x_between_edges_top_bottom = df.iloc[-1]['Distance_From_CenterEdge']
        theta_phi_list = self.get_theta(d3_hypotenuse_between_top_bottom, length_x_between_edges_top_bottom)        
        
        # About the top and furthest cyliners        
        height_z_top_to_furthest = topz1 - furthesstz1
        hypotenuse_top_to_furthest_cyl = height_z_top_to_furthest / math.cos(theta_phi_list[-1] * math.pi / 180)
        
        furthest_cyl_x_length = math.sqrt(hypotenuse_top_to_furthest_cyl**2 - height_z_top_to_furthest**2)
        
        furthest_cyl_point_on_line_coord = self.point_on_line_at_height((topx1, topy1, topz1), (bottomx1, bottomy1, bottomz1), furthesstz1)
        final_furthest_coord = self.get_final_furthest_coord((furthesstx1, furthessty1, furthesstz1), furthest_cyl_point_on_line_coord, furthest_cyl_x_length)
            
        print(final_furthest_coord)
        
        furthest_cylinders_info_dict = {"furthest_origin_edge_coord": (furthesstx1, furthessty1, furthesstz1),
                                        "furthest_estimate_on_linecoord": final_furthest_coord                                       
                                        }
        return furthest_cylinders_info_dict
    
    def get_ratio(self, df, dict):
        cylinders_info_height_sorted = df.sort_values(by='Height_Bin')
        sed = cylinders_info_height_sorted.iloc[-1]['MA_Diameter'] # Assume that the top cylinder has 'SED' which is Small End Diameter
        
        distance = math.sqrt((dict['furthest_estimate_on_linecoord'][0] - dict['furthest_origin_edge_coord'][0])**2 + (dict['furthest_estimate_on_linecoord'][1] - dict['furthest_origin_edge_coord'][1])**2)
        ratio = distance / sed
        
        
        return ratio
        
        
        
        
        
def main():
    
    parent_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_PlayGroundSet\Straightess_issue\SelectedSampleData'
    # laz_path = r'C:\Users\JooHyunAhn\Interpine\AssignedTasks\HQP - Genetic Trial\Straightess_issue\SelectedSampleData\Plot95_final_cyl_vis - Tree18.las'
    # csv_file_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_PlayGroundSet\Straightess_issue\SelectedSampleData\Plot95_18.csv'
    csv_file_path = r'C:\Users\JooHyunAhn\Interpine\DataSets\TreeTools_PlayGroundSet\Straightess_issue\Plot95_FT_output\taper\Plot95_12.csv'    
    
    ssObj = StraightnessScore(parent_path)    
    df = ssObj.read_csv(csv_file_path)
    
    # From this, top of 2d view
    derivated_df = ssObj.data_derivation(df)
    cylinders_info = ssObj.get_furthest_cylinders(derivated_df)
    hypotenuse, x_length, y_length = ssObj.get_length_hypotenuse_xy(cylinders_info[1])        
    theta_phi_list = ssObj.get_theta(hypotenuse, x_length)
    cylinders_edge_coords_df = ssObj.get_furthest_circumference_coordinates(cylinders_info, theta_phi_list)
    cylinders_info_height_sorted_df = ssObj.distances_add_from_edge(cylinders_edge_coords_df)
    
    # From this, side of 3d view
    furthest_cylinders_info_dict = ssObj.get_length_hypotenuse_3d_coord(cylinders_info_height_sorted_df)    
    print(furthest_cylinders_info_dict)
    ratio = ssObj.get_ratio(cylinders_info_height_sorted_df, furthest_cylinders_info_dict)
    print(ratio)


  
 
if __name__ == "__main__":
    main()