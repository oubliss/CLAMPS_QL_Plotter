# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 21:54:31 2021

@author: Marshall
"""
import cmocean
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt


#tyler's timeheight function
#tyler's timeheight function
cmaps = {
    'w'     : {'cm': 'seismic',   'label': 'vertical velocity [m/s]'},
    'wSpd'  : {'cm': 'gist_stern_r',              'label': 'windspeed [m/s]'},
    'wDir'  : {'cm': cmocean.cm.phase,   'label': 'wind direction [deg]'},
    'pt'    : {'cm': cmocean.cm.thermal, 'label': 'potential temperature [C]'},
    'temp'  : {'cm': cmocean.cm.thermal, 'label': 'temperature [C]'},
    'ptemp' : {'cm': cmocean.cm.thermal, 'label': 'potential temperature [C]'},
    'q'     : {'cm': cmocean.cm.haline_r,  'label': 'q [g/kg]'},
    'dewpt' : {'cm': cmocean.cm.haline_r,  'label': 'dewpoint [C]'},
    'rh'    : {'cm': cmocean.cm.haline_r,  'label': 'RH [%]'},
    'std'   : {'cm': cmocean.cm.thermal,  'label': 'Standard Deviation'},
    'bSc'   : {'cm': 'magma', 'label': 'Backscatter [log(10) space]'},
    'bSc_TALL' : {'cm': 'magma', 'label': 'Backscatter [log(10) space]'},
    'snr'   : {'cm': cmocean.cm.gray, 'label': 'Intensity (Signal to Noise Ratio)'}
}

def timeheight(time, height, data, field, ax, datemin=None, datemax=None,
                datamin=None, datamax=None, zmin=None, zmax=None, cmap=None, **kwargs):
    '''
    Produces a time height plot of a 2-D field
    :param time: Array of times (1-D or 2-D but must have same dimenstions as height)
    :param height: Array of heights (1-D or 2-D but must have same dimensions as time)
    :param data: Array of the data to plot (2-D)
    :param field: Field being plotted. Currently supported:
        'w': Vertical Velocity
        'ws': Wind Speed
        'wd': Wind Direction
        'pt': Potential Temperature
        'q':  Specific Humidity
        'dp': Dewpoint
        'rh': Relative Humidity
        'std': Standard Deviation
    :param ax: Axis to plot the data to
    :param datemin: Datetime object
    :param datemax: Datetime object
    :param datamin: Minimum value of data to plot
    :param datamax: Maximum value of data to plot
    :param zmin: Minimum height to plot
    :param zmax: Maximum height to plot
    :return:
    '''

    # Get the colormap and label of the data
    if cmap is None:
        cm, cb_label = cmaps[field]['cm'], cmaps[field]['label']
    else:
        cm, cb_label = cmap, cmaps[field]['label']

    # Convert the dates to matplolib format if not done already
    if time.ndim == 1 and height.ndim == 1:

        time = mdates.date2num(time)
        time, height = np.meshgrid(time, height)

    # Create the plot
    c = ax.pcolormesh(time, height, data, vmin=datamin, vmax=datamax, cmap=cm, **kwargs)

    # Format the colorbar
    # c.cmap.set_bad('grey', 1.0)
    cb = plt.colorbar(c, ax=ax)

    # Format the limits
    ax.xaxis.set_major_locator(mdates.HourLocator(interval = 2))
    ax.xaxis.set_minor_locator(mdates.HourLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
  
    if zmin is not None and zmax is not None:
        ax.set_ylim(zmin, zmax)
    if datemin is not None and datemax is not None:
        ax.set_xlim(mdates.date2num(np.array([datemin, datemax])))

    # Set the labels
    ax.set_ylabel('Height [m]', size = 18)
    ax.set_xlabel('Time [UTC]', size = 18)
    
    #setting fontsizes
    ax.tick_params(axis = 'x', labelsize = 16)
    ax.tick_params(axis = 'y', labelsize = 16) 
    cb.ax.tick_params(labelsize=16)
    cb.set_label(cb_label, size = 16)

    return ax