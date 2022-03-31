# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 11:57:16 2022

@author: Marshall
"""

def main():
    
    #do our imports
    import os
    import traceback as tb
    from netCDF4 import Dataset
    import Plotter
    
    from info_dicts import file_paths, data_info
    
    #if we just want to plot everything, set this to True
    plot_all_variables = True
    
    #get the data folder(s)
    CLAMPS_number = "C2"
    data_type = "dlfp"
    data_folders = file_paths['data'][CLAMPS_number][data_type]
    name_info = [CLAMPS_number, data_type]
    error_log_path = file_paths['error_log']
    
    #now that we have a list of folders, loop through list
    with open(error_log_path, 'w') as error_log: #error log will be DELETED on each new run
        for folder in data_folders:
            
            #get the names of the files in the folder
            files = os.listdir(folder)
            for file in files:
                
                #check if it's a valid netCDF file
                if Plotter.is_valid_file(file):
                    print(f"{file} accessed")
                    
                    #TEMPORARY CHECK
                    #check whether data is from the date range we want
                    #namely from 20210621 - 20210629
                    file_date = int(file[-19:-11])
                
                    if file_date <= 20230629 and file_date >= 20000621: #these new dates should encompass all possible dates in the files
                        try:
                            #format the file name into a full path
                            file_path = folder + "/" + file
                            
                            #get the data into a netCDF dataset object
                            data_netCDF4 = Dataset(file_path)
                            data = Plotter.yoink_the_data(data_netCDF4, name_info)
                            date = Plotter.date_from_filename(file)
                            
                            #access the datatype from the file that we want
                            if plot_all_variables:
                                
                                #the keys hold all of the possible variable types
                                variable_types = data_info[data_type].keys()
                                for variable in variable_types:
                                     Plotter.create_quicklook(variable, data, date, name_info)
                            
                            #TODO: Make functionality for plotting only some data
                            
                            #Close the dataset
                            data_netCDF4.close()
                        
                        except:
                            #catch the error and put it into a string
                            error_trace = tb.format_exc()
                            
                        else:
                            #no error, no problem
                            error_trace = 'No errors\n'
                            
                        finally:
                            #write to our error log
                            error_log.write(f"The following errors occured in {file}:\n")
                            error_log.write(error_trace)
                            
                            #this last one just separates the files
                            error_log.write("------------------------------\n")
                            
                            

if __name__ == "__main__":
    main()