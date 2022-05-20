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
    from helper_functions import get_QL_name
    from info_dicts import file_paths, data_info
    
    #if we just want to plot everything again, set these to True
    plot_all_variables = True
    remake_plots = True
    
    #List of quicklook types the user wants generated from the data_type
    variable_list = ["w_hs"] #only used if plot_all_variables = False
    
    #get the data folder(s)
    CLAMPS_number = "C2"
    data_type = "dlfp"
    data_folders = file_paths['data'][CLAMPS_number][data_type]
    name_info = [CLAMPS_number, data_type]
    error_log_path = file_paths['error_log']
    
    
    #optional range of dates in int of form yyyymmdd
    start_date = 20230629
    end_date = 20000621
    
    #now that we have a list of folders, loop through list
    with open(error_log_path, 'w') as error_log: #error log will be DELETED on each new run
        for folder in data_folders:
            
            #get the names of the files in the folder
            files = os.listdir(folder)
            for file in files:
                
                #check if it's a valid netCDF file
                if Plotter.is_valid_file(file):
                    print(f"{file} accessed")
                    
                    #check whether the file's date is in our predetermined range
                    file_date = int(file[-19:-11])
                    if file_date <= start_date and file_date >= end_date:
                        
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
                           
                            else:
                                #user defined variable types 
                                variable_types = variable_list
                                
                            #if the data doesn't have a variable, skip it and make note
                            data_variable_types = data.keys()
                            missing_data = []
                            
                            for variable in variable_types:
                                
                                #creating the path that a quicklook would be saved to
                                QL_filename = get_QL_name(CLAMPS_number, data_type, variable, date)
                                dump_folder_path = file_paths['dump'][CLAMPS_number][data_type]
                                dump_path = dump_folder_path + "/" + QL_filename
                                
                                #check whether a plot of this variable has already been made
                                if not os.path.exists(dump_path) or remake_plots:
                                    
                                    #check whether there is missing data if we're plotting everything
                                    if variable not in data_variable_types and plot_all_variables:
                                        missing_data.append(variable)
                                    else:
                                        Plotter.create_quicklook(variable, data, date, name_info)
                                        
                                else:
                                    continue
                            
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
                            
                            #bool of a non-empty list is true
                            if bool(missing_data):
                                missing_data_warn = "The following data is missing from the file: "
                                missing_data_types = ", ".join(missing_data)
                                
                                #adds message about missing data to the error log
                                error_log.write(f"{missing_data_warn}{missing_data_types}\n")
                                
                            error_log.write(error_trace)
                            
                            #this last one just separates the files
                            error_log.write("------------------------------\n")
                            
                            

if __name__ == "__main__":
    main()