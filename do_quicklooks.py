import os
import traceback as tb
import logging as log
from argparse import ArgumentParser
from glob import glob

from netCDF4 import Dataset

import Plotter
import do_timeseries
from helper_functions import get_QL_name
from info_dicts import file_paths, data_info


# Helper function
def check_bound(t, b):
    return (t >= b[0]) and (t <= b[1])




# Set up the argument parser
parser = ArgumentParser()
parser.add_argument('start_date', action='store', help="Start date in YYYYmmdd")
parser.add_argument('end_date', action='store', help="End date in YYYYmmdd")
parser.add_argument('facility', action='store', help='C1 or C2')
parser.add_argument('--realtime', action='store_true', default=False)
parser.add_argument('--clobber', action='store_true', default=False)
parser.add_argument('--debug', action='store_true', default=False)
args = parser.parse_args()

if args.debug:
    print("HELLO")
    log.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=log.DEBUG)

else:
    log.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=log.INFO)

# Extract the arguments
start_date = int(args.start_date)
end_date = int(args.end_date)
CLAMPS_number = args.facility

# Get all the data types from the config file
data_types = data_info.keys()

# Loop through each data type and plot them
for data_type in data_types:

    # if data_type == 'dlVAD':
    #     continue
    log.info(f"Working on data type {data_type}")
    # Get the data folders for this data type
    data_folders = file_paths['data'][CLAMPS_number][data_type]

    for folder in data_folders:
        log.info(f"  Working on folder {folder}")
        # Get the netcdf files from this folder
        files = glob(f"{folder}/*.cdf")

        # Find files between the start and end date
        files = [fn for fn in files if check_bound(int(fn[-19:-11]), (start_date, end_date))]

        for fn in sorted(files):
            if not Plotter.is_valid_file(fn):
                log.warning(f"Invalid file found: {fn}")
                continue

            log.debug(fn)

            name_info = [CLAMPS_number, data_type]
            nc = Dataset(fn)
            data = Plotter.yoink_the_data(nc, name_info)
            date = Plotter.date_from_filename(fn)
            nc.close()

            variable_types = data_info[data_type].keys()

            # if the data doesn't have a variable, skip it and make note
            data_variable_types = data.keys()
            missing_data = []
            print(data_variable_types)

            log.info(f"    Plotting file {fn}")
            for variable in variable_types:
                log.debug(f"Working on variable {variable}")

                # creating the path that a quicklook would be saved to
                QL_filename = get_QL_name(CLAMPS_number, data_type, variable, date)
                dump_folder_path = file_paths['dump'][CLAMPS_number][data_type]
                dump_path = dump_folder_path + "/" + QL_filename

                # Make sure the path exists
                if not os.path.exists(dump_folder_path):
                    log.info(f"Creating Path for images {dump_folder_path}")
                    os.makedirs(dump_folder_path)

                # If we don't want to clobber things, check for the file first
                if not args.clobber:
                    if os.path.exists(dump_path):
                        log.debug("  Skipping this file")
                        continue

                if variable in ['thermo', 'wind', 'rain_rate']:
                    print("HELLO")
                    do_timeseries.of(variable, data, date, name_info)
                    continue

                # check whether there is missing data if we're plotting everything
                if variable not in data_variable_types:
                    missing_data.append(variable)
                else:
                    try:

                        Plotter.create_quicklook(variable, data, date, name_info)
                    except Exception as e:
                        print(e)
                        log.error(f"    Error on file {fn.split('/')[-1]}: {variable}")
                        continue
