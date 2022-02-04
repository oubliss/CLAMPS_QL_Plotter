# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 11:57:16 2022

@author: Marshall
"""

def main():
    
    #do our imports
    import os
    from netCDF4 import Dataset
    import Plotter
    
    from info_dicts import file_paths, data_info
    
    #if we just want to plot everything, set this to True
    plot_all_variables = True
    
    #get the data folder(s)
    CLAMPS_number = "C1"
    data_type = "dlVAD"
    data_folders = file_paths['data'][CLAMPS_number][data_type]
    name_info = [CLAMPS_number, data_type]
    
    #now that we have a list of folders, loop through list
    for folder in data_folders:
        
        #get the names of the files in the folder
        files = os.listdir(folder)
        for file in files:
            
            #check if it's a valid netCDF file
            if Plotter.is_valid_file(file):
                
                #get the data into a netCDF dataset object
                data_netCDF4 = Dataset(file)
                data = Plotter.yoink_the_data(data_netCDF4, data_type)
                date = Plotter.date_from_filename(file)
                
                #access the datatype from the file that we want
                if plot_all_variables:
                    
                    #the keys hold all of the possible variable types
                    variable_types = data_info[data_type].keys()
                    for variable in variable_types:
                         Plotter.create_quicklook(variable, data, date, name_info)   
                        
                

if __name__ == "__main__":
    main()