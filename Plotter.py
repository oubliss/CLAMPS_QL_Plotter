# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:22:36 2021

@author: Marshall
"""

#official libraries
import numpy as np
from scipy.signal import find_peaks
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import math

#plotter-specific functions and dicts
from timeheight import timeheight
from info_dicts import data_info, file_paths
from helper_functions import uv_from_spd_dir, get_QL_name, get_snr_cutoff

class MidPointNormalize(Normalize):
    """Defines the midpoint of diverging colormap.
    Usage: Allows one to adjust the colorbar, e.g.
    using contouf to plot data in the range [-3,6] with
    a diverging colormap so that zero values are still white.
    Example usage:
        norm=MidPointNormalize(midpoint=0.0)
        f=plt.contourf(X,Y,dat,norm=norm,cmap=colormap)
     """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)
    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

#valid filename checker
def is_valid_file(data_filename):

    #checks whether file is a netCDF4 file
    is_cdf = "cdf" == data_filename[-3:]
    if is_cdf:

        #checks for error where seconds can be 60
        file_seconds = int(data_filename[-6:-4])
        if file_seconds < 60 and file_seconds >=0:
            return True

def date_from_filename(data_filename):

    date_string = data_filename[-19:-11]
    string_time_formatting = "%Y%m%d"
    date = datetime.strptime(date_string, string_time_formatting)

    return date


#data accessor function
#returns dictionary of all relevant data from dataset
def yoink_the_data(dataset, name_info):

    #for debugging pruposes
    #print("accessing data")
    CLAMPS_number = name_info[0]
    data_type = name_info[1]
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
        '''
        isnt_CLAMPS2 = CLAMPS_number != "C2" #
        if isnt_CLAMPS2:
            snr_cutoff = get_snr_cutoff(dataset, CLAMPS_number)
        else:
            CLAMPS2_snr_cutoff = 1.008
            snr_cutoff = CLAMPS2_snr_cutoff
        '''
        snr_cutoff = 1.008

        #find the index nearest 2500m
        max_height_idx = 0
        MAX_HEIGHT = 2500
        for hgt in height:
            if(hgt >=  MAX_HEIGHT):
                break
            max_height_idx += 1

        #converting backscatter data to logarithmic space and filtering by snr

        """
        for i in range(len(backscatter_TALL)):
            for j in range(len(backscatter_TALL[i])):
                if backscatter_TALL[i][j] > 0:
                    backscatter_TALL[i][j] = math.log10(backscatter_TALL[i][j])
                else:
                    backscatter_TALL[i][j] = np.nan
                if j < max_height_idx:
                    if intensity[i][j] < snr_cutoff:
                        w[i][j] = np.nan
        """
        backscatter_TALL = np.log10(backscatter_TALL)
        #backscatter_TALL = np.where(intensity < snr_cutoff, np.nan, np.log10(backscatter_TALL))
        w = np.where(intensity < snr_cutoff, np.nan, w)

        #ignore the first two gates of the doppler lidar and stop at 2500m
        height = height[2:]
        height_CUT = height[:max_height_idx-2] #the -2 is to compensate for the earlier cut
        w = w[:, 2:max_height_idx]
        intensity = intensity[:, 2:max_height_idx]
        backscatter_TALL = backscatter_TALL[:, 2:]
        backscatter = backscatter_TALL[:, :max_height_idx-2]

        return {"time": time,
                'w_hs': w,
                'w_ls': w,
                'snr': intensity,
                'bSc': backscatter,
                'bSc_TALL' : backscatter_TALL,
                'height_FULL': height,
                'height': height_CUT}

    if data_type == "aerioe":

        #get the times
        time = [datetime.utcfromtimestamp(d) for d in (dataset['base_time'][:]+dataset['time_offset'][:])]

        #sort the times
        sort = np.argsort(time)
        time = np.array(time)[sort]

        #get sorted data sources
        temp = dataset["temperature"][sort]
        ptemp = dataset["theta"][sort]
        dewpt = dataset["dewpt"][sort]
        wvmr = dataset["waterVapor"][sort]
        lwp = dataset["lwp"][sort]
        height = dataset["height"][:] * 1000

        #cbh and quality flag
        cbh = dataset["cbh"][sort] * 1000
        qcflag = dataset["qc_flag"][sort]
        rms = dataset["rmsa"][sort]
        hatch = dataset['hatchOpen'][sort]
        #find the index nearest 2500m
        num_sub2500_heights = len([h for h in height if h<2500])

        #remove first two gates
        height = height[:num_sub2500_heights]
        temp = temp[:, :num_sub2500_heights]
        ptemp = ptemp[:, :num_sub2500_heights]
        dewpt = dewpt[:, :num_sub2500_heights]
        wvmr = wvmr[:, :num_sub2500_heights]

        return {"time": time,
                'height': height,
                "cbh": cbh,
                "temp": temp,
                "ptemp": ptemp,
                "dewpt": dewpt,
                "wvmr": wvmr,
                "lwp": lwp,
                "rms": rms,
                "hatch": hatch,
                "qcflag": qcflag}

    if data_type == 'tower':

        # get the times
        time = [datetime.utcfromtimestamp(d) for d in (dataset['base_time'][:] + dataset['time_offset'][:])]

        # sort the times
        sort = np.argsort(time)
        time = np.array(time)[sort]

        # Extract the data
        temp = dataset['sfc_temp'][sort]
        rh = dataset['sfc_rh'][sort]
        pres = dataset['sfc_pres'][sort]
        pwv = dataset['pwv'][sort]
        lwp = dataset['lwp'][sort]
        rain_rate = dataset['rain_rate'][sort]
        sfc_wspd = dataset['sfc_wspd'][sort]
        sfc_wdir = dataset['sfc_wdir'][sort]

        # Calculate dewpoint
        def sat_vapor_pressure(T):
            """
            :param T: T in degrees C
            :return:
            """
            return 6.112 * np.exp(17.67 * T / (T + 243.5))

        def dewpoint(e):
            """
            returns Td in C
            :param e:
            :return:
            """
            return 243.5 * np.log(e / 6.112) / (17.67 - np.log(e / 6.112))

        dwpt = dewpoint(rh / 100 * sat_vapor_pressure(temp))

        return {"time": time,
                "temp": temp-273.15,
                "rh": rh,
                "dwpt": dwpt-273.15,
                "pres": pres,
                "pwv": pwv,
                "lwp": lwp,
                "rain_rate": rain_rate,
                "wspd": sfc_wspd,
                "wdir": sfc_wdir
                }



time_formatting = "%Y%m%d"
def create_quicklook(data_type, data, date, name_info, #name info should be a list with [facility, file_type]
                     figHeight = 5, figWidth =15, realtime=False):     

    #parse name_info list
    CLAMPS_number = name_info[0]
    data_source = name_info[1]

    #create figure and set dimensions
    fig, ax = plt.subplots(1)
    fig.set_figheight(figHeight)
    fig.set_figwidth(figWidth)

    #make grid
    if data_type == "bSc_TALL":
        timeGrid, heightGrid = np.meshgrid(data["time"], data["height_FULL"])
        zmax = round(data["height_FULL"][-1], -3) #rounds to nearest thousandth
    else:
        timeGrid, heightGrid = np.meshgrid(data["time"], data["height"])
        zmax = 2500

    norm = None
    if data_type == 'temp':
        norm = MidPointNormalize(midpoint=0.0)


    #use timeheight function to plot data
    ax = timeheight(timeGrid, heightGrid, data[data_type].transpose(), data_type, ax=ax,
                    datamin = data_info[data_source][data_type]['datamin'],
                    datamax = data_info[data_source][data_type]['datamax'],
                    zmin = 0, zmax = zmax, zorder = 1, norm=norm)

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
    def qc_aeri(data): #returns good and maybe indices for cbh based on qcflag
        hatch_closed_indices = []
        skeptical_indices = []
        cbh_indices = []

        for i in range(len(data["time"])):
            if data["rms"][i] > 10:
                skeptical_indices.append(i)

            if data['lwp'][i] > 3:
                cbh_indices.append(i)

            if data['hatch'][i] < 1:
                hatch_closed_indices.append(i)


            """
            if data["qcflag"][i] == 0:
                good_cbh_indices.append(i)
            elif data["qcflag"][i] == 3:
                skeptic_cbh_indices.append(i)
            """

        return {
                "hatch"    : hatch_closed_indices,
                "qc" : skeptical_indices,
                "cbh": cbh_indices
                }

    if data_type in ['temp', 'ptemp', 'dewpt', 'wvmr']:
        indices = qc_aeri(data)
        ax.plot(data["time"][indices["cbh"]], data["cbh"][indices["cbh"]],
                linestyle = "None", markersize = 10, color = 'k', marker='.')

        ax.plot(data["time"][indices["hatch"]], np.full_like(data["time"][indices["hatch"]], 2500*.98),
                 linestyle = "None", markersize = 10, color = 'red', marker='.')

        """
        ax.plot(data["time"][cbh_indices["good_cbh_indices"]], data["cbh"][cbh_indices["good_cbh_indices"]],
                linestyle = "None", markersize = 10, color = 'pink', zorder = 2)
        ax.plot(data["time"][cbh_indices["skeptic_cbh_indices"]], data["cbh"][cbh_indices["skeptic_cbh_indices"]],
                linestyle = "None", markersize = 10, color = 'pink', zorder = 3)
        """

    #setting x-axis limits
    seed_date = timeGrid[0][0].date()
    start_datetime = datetime(year = seed_date.year,
                              month = seed_date.month,
                              day = seed_date.day)
    end_datetime = start_datetime + timedelta(days=1)
    ax.set_xlim([start_datetime, end_datetime])

    #setting the plot background color
    ax.set_facecolor((.9,.9,.9)) #light grey

    #set title
    ax.set_title("{} {} -- {}".format(data_info[data_source][data_type]['name'],
                                      CLAMPS_number, date.isoformat()), fontsize = 22)

    #tighten up the layout
    plt.tight_layout()

    #save figure
    facility = CLAMPS_number
    file_type = data_source

    dump_folder_path = file_paths['dump'][facility][file_type]
    # filename = get_QL_name(facility, file_type, data_type, start_datetime)

    # dump_path = dump_folder_path + "/" + filename

    if realtime:
        filename = get_QL_name(facility, file_type, data_type, start_datetime, realtime)
        
        # Get realtime dates
        end_time = datetime.utcnow()
        td = [6, 24]

        for fn, t in zip(filename, td): 
            
            # Redo the x-limits
            ax.set_xlim([end_time-timedelta(hours=t), end_time])

            # Redo the title
            ax.set_title("{} {} -- {}".format(data_info[data_source][data_type]['name'],
                                      CLAMPS_number, f"Last {t} Hours"), fontsize = 22)

            dump_path = dump_folder_path + "/" + fn
            # print(dump_path)
            plt.savefig(dump_path)
    else:
        filename = get_QL_name(facility, file_type, data_type, start_datetime)
        dump_path = dump_folder_path + "/" + filename
        # print(dump_path)
        plt.savefig(dump_path)

    #close the plot
    plt.close()













