# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:22:36 2021

@author: Marshall
"""

#official libraries
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import os
from netCDF4 import Dataset
import math

#plotter-specific functions and dicts
from timeheight import timeheight
from info_dicts import valid_filename_info, data_info, file_paths
from helper_functions import uv_from_spd_dir, get_QL_name, get_snr_cutoff

#TODO: this needs to be fleshed out into a regex function to get the filename parameters
#use in to access data type i.ie. if "dlvad" in filename
#go backwards for facility
def parse_filename(filename):
    
    #ignoring non-data files
    if "cdf" in filename:

        facility = filename[-25:-23] # C1 or C2
        
        if facility == "C1":
            if "dlfp" in filename:
                return ["C1", "dlfp"]
            elif "dlvad" in filename:
                return ["C1", "dlVAD"]
        
        if facility == "C2":
            if "dlfp" in filename:
                return ["C2", "dlfp"]
            elif "dlvad" in filename:
                return ["C2", "dlVAD"]
        
        
#valid filename checker
def is_valid_file(data_filename):
    
    #checks whether file is a netCDF4 file
    is_cdf = "cdf" == data_filename[-3:]
    if is_cdf:
        
        #checks for error where seconds can be 60
        file_seconds = int(data_filename[-6:-4])        
        if file_seconds < 60 and file_seconds >=0:
            return True
        

#data accessor function
#returns dictionary of all relevant data from dataset
def yoink_the_data(dataset, data_type):
    
    #for debugging pruposes
    print("accessing data")
    
    if data_type == 'dlVAD':
        #get the times
        time = [datetime.utcfromtimestamp(d) for d in (dataset['base_time'][:]+dataset['time_offset'][:])]
        
        #sort the times
        sort = np.argsort(time)
        time = np.array(time)[sort]
        
        #get sorted data sources
        wspd = dataset['wspd'][sort]
        wdir = dataset['wdir'][sort]
        height  = dataset['height'][:] * 1000
        
        # The first two gates of the Doppler lidar are usually bad data, so ignore the first two heights
        height = height[2:]
        wspd = wspd[:, 2:]
        wdir = wdir[:, 2:]  
        
        #convert wind speed to u and v components
        
        u, v = uv_from_spd_dir(wspd, wdir)
        
        #returns dictionary of all required data
        return {"time": time,
                'height': height,
                'wSpd': wspd,
                'wDir' : wdir,
                'u' : u,
                'v' : v}
    
    if data_type == 'dlfp':
        #get the times
        time = [datetime.utcfromtimestamp(ts) for ts in dataset['base_time'][:]+dataset['time_offset'][:]]
    
        #sort the times
        sort = np.argsort(time) #this gives the indices that would sort the time array
        time = np.array(time)[sort]
    
        #get sorted data sources
        w = dataset['velocity'][sort]
        intensity = dataset['intensity'][sort]
        backscatter_TALL = dataset['backscatter'][sort]
        height = dataset['height'][:] * 1000 #conversion to meters
        
        #computes a dynamic snr cutoff 
        snr_cutoff = get_snr_cutoff(dataset)
        
        #find the index nearest 2500m
        max_height_idx = 0
        MAX_HEIGHT = 2500
        for hgt in height:
            if(hgt >=  MAX_HEIGHT):
                break
            max_height_idx += 1
        
        #converting backscatter data to logarithmic space and filtering by snr
        for i in range(len(backscatter_TALL)):
            for j in range(len(backscatter_TALL[i])):
                if backscatter_TALL[i][j] > 0:
                    backscatter_TALL[i][j] = math.log10(backscatter_TALL[i][j])
                else:
                    backscatter_TALL[i][j] = np.nan
                if j < max_height_idx:
                        if intensity[i][j] < snr_cutoff:
                            w[i][j] = np.nan  
                            
        #ignore the first two gates of the doppler lidar and stop at 2500m
        height = height[2:]
        height_CUT = height[:max_height_idx-2] #the -2 is to compensate for the earlier cut
        w = w[:, 2:max_height_idx]
        intensity = intensity[:, 2:max_height_idx]
        backscatter_TALL = backscatter_TALL[:, 2:]
        backscatter = backscatter_TALL[:, :max_height_idx-2]
    
        return {"time": time,
                'w': w,
                'snr': intensity,
                'bSc': backscatter,
                'bSc_TALL' : backscatter_TALL,
                'height_FULL': height,
                'height': height_CUT}

    if data_type == "aeri":
        
        #get the times
        time = [datetime.utcfromtimestamp(d) for d in (dataset['base_time'][:]+dataset['time_offset'][:])]
        
        #sort the times
        sort = np.argsort(time)
        time = np.array(time)[sort]
        
        #get sorted data sources
        temp = dataset["temperature"][sort]
        ptemp = dataset["theta"][sort]
        dewpt = dataset["dewpt"][sort]
        height = dataset["height"][:] * 1000        
 
        #cbh and quality flag
        cbh = dataset["cbh"][:] * 1000
        qcflag = dataset["qc_flag"][:]
        
        #find the index nearest 2500m
        max_height_idx = 0
        MAX_HEIGHT = 2500
        for hgt in height:
            if(hgt >=  MAX_HEIGHT):
                break
            max_height_idx += 1
        
        
        #remove first two gates
        height = height[2:max_height_idx]
        temp = temp[:, 2:max_height_idx]
        ptemp = ptemp[: 2:max_height_idx]
        dewpt = dewpt[:, 2:max_height_idx]

        return {"time": time,
                'height': height,
                "cbh": cbh,
                "temp": temp,
                "ptemp": ptemp,
                "dewpt": dewpt,
                "qcflag": qcflag}
        
        
        
time_formatting = "%Y%m%d"
def create_quicklook(data_type, data, date, name_info, #name info should be a
                     figHeight = 5, figWidth =15):                           #list with [facility, file_type]
      
    #create figure and set dimensions
    fig, ax = plt.subplots(1)
    fig.set_figheight(figHeight)
    fig.set_figwidth(figWidth)

    #make grid
    if data_type = "bSc_TALL":
        timeGrid, heightGrid = np.meshgrid(data["time"], data["height_FULL"])
    else:
        timeGrid, heightGrid = np.meshgrid(data["time"], data["height"])
    
    #use timeheight function to plot data
    ax = timeheight(timeGrid, heightGrid, data[data_type].transpose(), data_type, ax=ax,
                    datamin = data_info[data_type]['datamin'],
                    datamax = data_info[data_type]['datamax'],
                    zmin = 0, zmax = 2500, zorder = 1)
    
    if data_type == 'wDir':
        
        u = data["u"]
        v = data["v"]
        
        #filter the wind components
        u = np.where(np.abs(u) < 50, u, np.nan)
        v = np.where(np.abs(v) < 50, v, np.nan)
        
        #TODO: determine frequency of wind barbs (reduced height range complicates this)
        skipx = len(data['wSpd'][0]) // 40
        skipy = len(data['wSpd']) // 15
        
        ax.barbs(timeGrid[::skipx, ::skipy],
                 heightGrid[::skipx, ::skipy],
                 u.transpose()[::skipx, ::skipy],
                 v.transpose()[::skipx, ::skipy])
    
    #adding cbh
    if data_type == 'temp' or data_type == 'ptemp':
        ax.plot(time, cbh, linestyle = "-", markersize = 20, linewidth = 6, color = 'pink', zorder = 2)
    elif data_type == 'dewpt':
        ax.plot(time, cbh, linestyle = "-", markersize = 20, linewidth = 6, color = '#90ee90', zorder = 2)
    
    #setting x-axis limits
    seed_date = timeGrid[0][0].date()
    start_datetime = datetime(year = seed_date.year,
                              month = seed_date.month,
                              day = seed_date.day)
    end_datetime = start_datetime + timedelta(days=1)
    
    ax.set_xlim([start_datetime, end_datetime])

    #set title
    ax.set_title("{} -- {}".format(data_info[data_type]['name'], date.isoformat()), fontsize = 22)
    
    #save figure
    facility = name_info[0]
    file_type = name_info[1]
    
    dump_folder_path = file_paths['dump'][facility][file_type]
    filename = get_QL_name(facility, file_type, data_type, start_datetime)
    
    dump_path = dump_folder_path + "/" + filename
    
    plt.savefig(dump_path)
    
    #close the plot
    plt.close()
    
        
        
    
    
    
    
    
    
    
    
    
    