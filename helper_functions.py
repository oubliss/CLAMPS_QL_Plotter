# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:44:41 2021

@author: Marshall
"""
import numpy as np
import matplotlib as mpl
from datetime import datetime

def add_blank_colorbar(fig):
    cmap = (mpl.colors.ListedColormap([(0., 0., 0., 0.)]))
    bounds = [0, 1]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))

    return cb

def uv_from_spd_dir(speed, wdir):
    wdir = np.deg2rad(wdir)
    u = -speed * np.sin(wdir)
    v = -speed * np.cos(wdir)
    return u, v

def get_QL_name(facility, data_source, data_type, date, realtime=False):
    
    if isinstance(date, int):
        date_str = str(date)
    else:
        date_format = "%Y%m%d"
        date_str = datetime.strftime(date, date_format)
    
    if realtime:
        name = [f"QL.{facility}.{data_source}.{data_type}.last_06_hours.png",
                f"QL.{facility}.{data_source}.{data_type}.last_24_hours.png"]
    else:
        name = f"QL.{facility}.{data_source}.{data_type}.{date_str}.png"
    
    return name

def get_snr_cutoff(data, CLAMPS_number):
    
    import statistics as st
    
    w_T = data['velocity'][:].transpose()
    w_flat = np.array(w_T[2:83]).flatten()
    
    snr_T = data['intensity'][:].transpose()
    snr_flat = np.array(snr_T[2:83]).flatten()
    
    #APPROACH
    #bin the w's into buckets of width .002 snr
    #once those bins have been established, calculate the std dev of velocities
    #plot these std devs. Then calculate the finite-difference approximations
    
    print("Determining snr cutoff")
    
    #creating a random sample size so my code doesn't take ungodly amounts of time
    subsample_size = len(snr_flat)//200
    rand_indices = np.random.randint(0, len(snr_flat), size = subsample_size)
    snr_flat = np.array([snr_flat[i] for i in rand_indices])
    w_flat = np.array([w_flat[i] for i in rand_indices])
    
    #sorting our snr's and w's
    sort = np.argsort(snr_flat)
    snr_flat = snr_flat[sort]
    w_flat = w_flat[sort]
    
    #binning
    snr_step = .002
    bins = np.arange(1, 1.1-8*snr_step, snr_step)
    w_bins = [ [] for _ in range(len(bins))]
    
    bucket_num = 0    
    
    for i in range(len(snr_flat)):
        #if the snr is less than the value for the bucket cutoff
        if snr_flat[i] < bins[bucket_num]:
                
            #add the corresponding w value
            w_bins[bucket_num].append(float(w_flat[i]))
            
        else: #since it's sorted, we can go straight to the next upper bound
            bucket_num += 1
            if bucket_num == len(bins): #if we're done with bins, break
                break
    
    w_stdevs = []
    
    for w_list in w_bins:
        if len(w_list) > 1:
            w_stdevs.append(st.stdev(w_list))
        else:
            w_stdevs.append(np.NaN)
            
    stdev_derivs_diff = []
    for idx in range(len(w_stdevs)-1): #-1 since we will use an idx + 1 for differences
        
        #find the difference between current element and next
        x0 = w_stdevs[idx]
        x1 = w_stdevs[idx + 1]
        
        deriv = (x1 - x0) / snr_step
        
        stdev_derivs_diff.append(deriv)
    
    #create boolean to record whether the standard devation has narrowed
    stdev_has_decreased = False
    
    #TODO: Undo this gross hard coding so we can add more CLAMPS systems
    if CLAMPS_number == "C2":
        loose_cutoff = True
    else:
        loose_cutoff = False
    
    for idx in range(len(stdev_derivs_diff) - 1):
    
        if not stdev_has_decreased:
            if stdev_derivs_diff[idx] < -200:
                stdev_has_decreased = True
        else: 
            if abs(stdev_derivs_diff[idx]) < 100 and abs(stdev_derivs_diff[idx+1]) < 100:
                snr_cutoff = bins[idx]
                if loose_cutoff:
                    snr_cutoff = bins[idx - 2] #for CLAMPS2
                break
    
    return snr_cutoff
