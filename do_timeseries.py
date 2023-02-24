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


def of(data_type, data, date, name_info):

    CLAMPS_number = name_info[0]
    data_source = name_info[1]

    start_datetime = date
    end_datetime = date + timedelta(days=1)

    if data_type == 'tower':

        fig_height = 10
        fig_width = 15

        fig, (thermo_ax, wind_ax) = plt.subplots(2, sharex=True, figsize=(fig_width, fig_height))

        thermo_ax.plot(data['time'], data['temp'], 'maroon')
        thermo_ax.fill_between(data['time'], data['temp'], data['dwpt'], color='maroon', alpha=.5)
        thermo_ax.plot(data['time'], data['dwpt'], 'royalblue')
        thermo_ax.fill_between(data['time'], data['dwpt'], -273, color='royalblue', alpha=.5)
        thermo_ax.set_title("{} {} -- {}".format(data_info[data_source][data_type]['name'],
                                      CLAMPS_number, date.isoformat()), fontsize = 22)
        thermo_ax.set_ylabel("Temperature/Dewpoint [C]")
        thermo_ax.set_ylim((np.min(data['dwpt']-5), np.max(data['temp']+5)))
        thermo_ax.grid()

        wind_ax2 = wind_ax.twinx()
        wind_ax.plot(data['time'], data['wspd'], 'royalblue')
        wind_ax.set_ylabel("Wind Speed [m/s]")

        wind_ax2.plot(data['time'], data['wdir'], 'k*', markersize=1)
        wind_ax2.set_ylabel("Wind Direction [deg]")
        wind_ax2.set_ylim(0, 360)

        thermo_ax.set_xlim([start_datetime, end_datetime])
        wind_ax.set_xlim([start_datetime, end_datetime])
        wind_ax.grid()

        # Format the limits
        wind_ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        wind_ax.xaxis.set_minor_locator(mdates.HourLocator())
        # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        wind_ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
        plt.setp(wind_ax.xaxis.get_majorticklabels(), rotation=45)

    else:
        pass

    # tighten up the layout
    plt.tight_layout()

    # save figure
    facility = CLAMPS_number
    file_type = data_source

    dump_folder_path = file_paths['dump'][facility][file_type]
    filename = get_QL_name(facility, file_type, data_type, start_datetime)

    dump_path = dump_folder_path + "/" + filename

    print(dump_path)
    plt.savefig(dump_path)

    # close the plot
    plt.close()








