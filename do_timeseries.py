import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from datetime import datetime, timedelta

from info_dicts import data_info, file_paths
from helper_functions import get_QL_name


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

    # save figure
    facility = CLAMPS_number
    file_type = data_source

    dump_folder_path = file_paths['dump'][facility][file_type]
    if realtime:
        print("Realtime")
        filename = get_QL_name(facility, file_type, data_type, start_datetime, realtime)
        
        for fn in filename: 
            dump_path = dump_folder_path + "/" + fn
            print(dump_path)
            plt.savefig(dump_path)
    else:
        filename = get_QL_name(facility, file_type, data_type, start_datetime)
        dump_path = dump_folder_path + "/" + filename
        print(dump_path)
        plt.savefig(dump_path)
        

    

    # close the plot
    plt.close()








