import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colorbar as cbar
import matplotlib as mpl
import numpy as np

from datetime import datetime, timedelta

from info_dicts import data_info, file_paths
from helper_functions import get_QL_name, add_blank_colorbar


def do_lwp():
    return


def do_mwr_housekeeping():
    return


def of(data_type, data, date, name_info, realtime=False):

    CLAMPS_number = name_info[0]
    data_source = name_info[1]

    if not realtime:
        start_datetime = date
        end_datetime = date + timedelta(days=1)
    else:
        end_datetime = datetime.utcnow()
        start_datetime = end_datetime - timedelta(hours=6)

    fig_height = 5
    fig_width = 15
    fig, (ax) = plt.subplots(1, figsize=(fig_width, fig_height))

    cb = None
    if data_type == 'thermo':

        ax.plot(data['time'], data['temp'], 'maroon')
        ax.fill_between(data['time'], data['temp'], data['dwpt'], color='maroon', alpha=.5)
        ax.plot(data['time'], data['dwpt'], 'royalblue')
        ax.fill_between(data['time'], data['dwpt'], -273, color='royalblue', alpha=.5)
        ax.set_title("{} {} -- {}".format(data_info[data_source][data_type]['name'],
                                      CLAMPS_number, date.isoformat()), fontsize = 22)
        ax.set_ylabel("Temperature/Dewpoint [C]", size=18)
        ax.set_ylim((np.min(data['dwpt']-5), np.max(data['temp']+5)))
        ax.grid()
        ax.set_xlim([start_datetime, end_datetime])

        cb = add_blank_colorbar(fig)

    elif data_type == 'wind':

        ax2 = ax.twinx()
        ax.plot(data['time'], data['wspd'], 'royalblue')
        ax.set_ylabel("Wind Speed [m/s]", size=18)

        ax2.plot(data['time'], data['wdir'], 'k*', markersize=1)
        ax2.set_ylabel("Wind Direction [deg]", size=18)
        ax2.set_ylim(0, 360)

        ax.set_xlim([start_datetime, end_datetime])
        ax.grid()

        ax2.tick_params(axis='y', labelsize=16)

        # cb, kwargs = cbar.make_axes(ax)
        cb = add_blank_colorbar(fig)

    elif data_type == "rain_rate":

        ax.plot(data['time'], data['rain_rate'], 'royalblue')
        ax.fill_between(data['time'], data['rain_rate'], 0, color='royalblue', alpha=.5)
        ax.set_ylabel("Rain Rate[mm/hr]", size=18)
        ax.set_xlim([start_datetime, end_datetime])
        ax.set_ylim(0, np.max(data['rain_rate']+5))
        ax.grid()

        cb = add_blank_colorbar(fig)
    
    elif data_type == "lwp_pwv":
        if 'pwv' not in data.keys():  # This will kick it out if we're looking at the .a0. file
            plt.close()
            return

        ax2 = ax.twinx()
        ax.plot(data['time'], data['pwv'], 'royalblue')
        ax.set_ylabel("PWV [g/m2]", size=18)
        ax.set_ylim(0, 50)

        ax2.plot(data['time'], data['lwp'], 'crimson')
        ax2.set_ylabel("LWP [kg/m2]", size=18)
        ax2.set_ylim(-50, 250)

        ax.set_xlim([start_datetime, end_datetime])
        ax.grid()

        ax2.tick_params(axis='y', labelsize=16)

        # cb, kwargs = cbar.make_axes(ax)
        cb = add_blank_colorbar(fig)

    elif data_type == "stability":
        if 'recstable1' not in data.keys():  # This will kick it out if we're looking at the .a1. file
            plt.close()
            return

        ax.plot(data['time'], data['recstable1'], 'crimson', label="Reciever 1")
        ax.plot(data['time'], data['recstable2'], 'royalblue', label="Reciever 2")
        ax.legend()
        ax.set_xlim([start_datetime, end_datetime])
        ax.set_ylabel("Stability [mK]", size=18)
        ax.set_ylim(0, 20)

        cb = add_blank_colorbar(fig)

    elif data_type == "cooler_detector":

        if "detectorTemp" not in data.keys():
            plt.close()
            return
        
        ax2 = ax.twinx()

        ax.plot(data['time'], data['coolerCurrent'], 'royalblue', label='Cooler Current')
        ax.set_ylabel("Cooler Current [mA]", size=18)
        ax.set_ylim(0, 0.5)
        ax.set_xlim([start_datetime, end_datetime])

        ax2.plot(data['time'], data['detectorTemp'], 'crimson', label='Detector temperature')
        ax2.set_ylabel("Detector Temperatuer [K]", size=18)
        ax2.set_ylim(70, 85)

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc = 7, bbox_to_anchor=(1.2, .5))

        cb = add_blank_colorbar(fig)

    elif data_type == "system_temps":
        
        if "calibrationAmbientTemp" not in data.keys():
            plt.close()
            return
        

        # Do a bunch of crazy stuff to figure out some good bounds
        foo = [np.nanpercentile(data['calibrationCBBtemp'], [5, 95]), 
               np.nanpercentile(data['airNearInterferometerTemp'], [5, 95]), 
               np.nanpercentile(data['outsideAirTemp'], [5, 95]),
               np.nanpercentile(data['airNearBBsTemp'], [5, 95]), 
               np.nanpercentile(data['calibrationAmbientTemp'], [5, 95])]

        foo0 = np.where((data['calibrationCBBtemp'] > foo[0][0]) & (data['calibrationCBBtemp'] < foo[0][1]))
        foo1 = np.where((data['airNearInterferometerTemp'] > foo[1][0]) & (data['airNearInterferometerTemp'] < foo[1][1]))
        foo2 = np.where((data['outsideAirTemp'] > foo[2][0]) & (data['outsideAirTemp'] < foo[2][1]))
        foo3 = np.where((data['airNearBBsTemp'] > foo[3][0]) & (data['airNearBBsTemp'] < foo[3][1]))
        foo4 = np.where((data['calibrationAmbientTemp'] > foo[4][0]) & (data['calibrationAmbientTemp'] < foo[4][1]))
        
        foo = np.concatenate([data['calibrationCBBtemp'][foo0], 
               data['airNearInterferometerTemp'][foo1], 
               data['outsideAirTemp'][foo2],
               data['airNearBBsTemp'][foo3], 
               data['calibrationAmbientTemp'][foo4]])
                
        minv = np.nanmin(foo)
        maxv = np.nanmax(foo)
        meanv = np.mean([minv, maxv]) 


        minv -= minv % 10
        maxv += 10 - maxv%10
        delta = (maxv-minv)/20

        # Figure out the QC Flag and hatch closed
        hbb_nen_thresh = 0.05			# Thresholds from the qc_aeri script
        irad_thres    = 0.1		
        qc_ind = np.where((data['LW_HBB_NEN'] > hbb_nen_thresh) | (np.abs(data['skyViewImaginaryRadiance2510_2515'] > irad_thres)))
        hatch_ind = np.where(data['hatchOpen'] != 1)


        # Finally do the plot
        ax.plot(data['time'], data['calibrationCBBtemp'], 'royalblue', label='ABB')
        ax.plot(data['time'], data['calibrationHBBtemp'] - np.nanmean(data['calibrationHBBtemp']) + meanv, 'crimson', 
                label=f"HBB (-{np.round(np.nanmean(data['calibrationHBBtemp']) - meanv)})")
        ax.plot(data['time'], data['outsideAirTemp'], 'powderblue', label='Outside')
        ax.plot(data['time'], data['airNearBBsTemp'], 'gold', label='Near BB')
        ax.plot(data['time'], data['calibrationAmbientTemp'], 'forestgreen', label='Reflected')
        ax.plot(data['time'], data['airNearInterferometerTemp'], 'k', label='Interferometer')

        ax.scatter(data['time'][qc_ind], np.full_like(data['time'][qc_ind], maxv-delta), color='red', marker='*', label="QC Questionable", zorder=2)
        ax.scatter(data['time'][hatch_ind], np.full_like(data['time'][hatch_ind], minv+delta), color='purple', marker='*', label="Hatch Closed", zorder=2)

        ax.set_xlim([start_datetime, end_datetime])
        ax.set_ylim([minv, maxv])
        ax.set_ylabel("Temperature [K]", size=18)    

        cb = add_blank_colorbar(fig)
        ax.grid()
        ax.legend(loc = 7, bbox_to_anchor=(1.2, .5))

    elif data_type == 'inside_outside_temps':
        if "outsideAirTemp" not in data.keys():
            plt.close()
            return 
        
        tmp = np.concatenate([data['outsideAirTemp'],data['rackAmbientTemp']])-273.16
        minv = (int(np.nanmin(tmp)) / 5 + 0) * 5
        maxv = (int(np.nanmax(tmp)) / 5 + 1) * 5
        
        ax.plot(data['time'], data['outsideAirTemp']-273, 'powderblue', label='Outside Temp')
        ax.plot(data['time'], data['rackAmbientTemp']-273, 'crimson', label='Inside Temp')
        ax.set_xlim([start_datetime, end_datetime])
        ax.set_ylim([minv, maxv])
        ax.set_ylabel("Temperature [C]", size=18)   

        ax.legend(loc = 7, bbox_to_anchor=(1.2, .5))
        ax.grid()

        cb = add_blank_colorbar(fig)

    elif data_type == 'aeri_brightness_temps':
        if "outsideAirTemp" not in data.keys():
            plt.close()
            return 
        
        # Figure out the QC Flag and hatch closed
        hbb_nen_thresh = 0.05			# Thresholds from the qc_aeri script
        irad_thres    = 0.1		
        qc_ind = np.where((data['LW_HBB_NEN'] > hbb_nen_thresh) | (np.abs(data['skyViewImaginaryRadiance2510_2515'] > irad_thres)))
        hatch_ind = np.where(data['hatchOpen'] != 1)

        maxv = np.nanmax(data['surfaceLayerAirTemp675_680'])
        maxv = (int(maxv) / 10 + 1) * 10
        minv = 200
        delta = (maxv-minv)/20

        ax.plot(data['time'], data['surfaceLayerAirTemp675_680'], 'crimson', label='SfcAir 675cm{^-1}')
        ax.plot(data['time'], data['longwaveWindowAirTemp985_990'], 'royalblue', label='WinAir 985cm{^-1}')
        ax.plot(data['time'], data['shortwaveWindowAirTemp2510_2515'], 'forestgreen', label='WinAir 2510cm{^-1}')

        ax.scatter(data['time'][qc_ind], np.full_like(data['time'][qc_ind], maxv-delta), color='red', marker='*', label="QC Questionable", zorder=2)
        ax.scatter(data['time'][hatch_ind], np.full_like(data['time'][hatch_ind], minv+delta), color='purple', marker='*', label="Hatch Closed", zorder=2)

        
        ax.set_xlim([start_datetime, end_datetime])
        ax.set_ylim([minv, maxv])
        ax.set_ylabel("Temperature [C]", size=18) 
        ax.legend(loc = 7, bbox_to_anchor=(1.2, .5))
        
        cb = add_blank_colorbar(fig)


    else:
        pass

    # Format the limits
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_minor_locator(mdates.HourLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    # Set the labels
    ax.set_xlabel('Time [UTC]', size=18)

    # setting fontsizes
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

    # tighten up the layout
    plt.tight_layout()

    if cb is not None:  # Need to do this after tight_layout() so things don't get wonky
        cb.ax.axison = False
        cb.outline.set_edgecolor((0,0,0,0))
        cb.ax.zorder = -1

    # save figure
    facility = CLAMPS_number
    file_type = data_source

    dump_folder_path = file_paths['dump'][facility][file_type]
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
        print(dump_path)
        plt.savefig(dump_path)
        

    

    # close the plot
    plt.close()








