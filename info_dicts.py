# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 18:56:36 2021

@author: Marshall
"""

# plot_base_dir = "/raid/clamps/reprocessing/quicklooks/"
#plot_base_dir = "/www/apps.nssl.noaa.gov/clamps-test/CLAMPS_website/plots"
plot_base_dir = "/Users/clamps/data/plots"

data_info = {
    'aerioe': {
        'ptemp'      : {'name': 'Potential Temperature', 'datamax': 320, 'datamin':290},
        'temp'       : {'name': 'Temperature', 'datamax': 30, 'datamin': -20},
        'dewpt'      : {'name': 'Dewpoint', 'datamax': 25, 'datamin': -15},
        'wvmr'       : {'name': 'Water Vapor Mixing Ratio', 'datamax': 20, 'datamin': 0}
        },

    'tower': {
        'thermo'      : {'name': 'MWR Tower'},
        'wind'        : {'name': 'MWR Tower'},
        'rain_rate'   : {'name': 'MWR Tower'},
        },
    
    'mwr': {
        'lwp_pwv'     : {'name': "MWR LWP/PWV"},
        'stability'   : {'name': "MWR Stability"}
    },

    'housekeeping': {
        'cooler_detector'       : {'name': "AERI Cooler/Dectector"},
        'system_temps'          : {'name': "AERI System Temps"},
        'inside_outside_temps'  : {'name': "AERI Inside/Outside Temps"},
        'aeri_brightness_temps' : {'name': "AERI Brightness Temps"}
    },

    'dlVAD' : {
        'wSpd'    : {'name': 'Wind Speed', 'datamax':30,  'datamin':0},
        'wDir'    : {'name': 'Wind Direction', 'datamax':360, 'datamin':0}
        },

    'dlfp'  : {
        'w_hs'       : {'name': 'Vertical Velocity (High Sensitivity)', 'datamax': 2, 'datamin': -2},
        'w_ls'       : {'name': 'Vertical Velocity (Low Sensitivity)', 'datamax': 5, 'datamin': -5},
        'bSc'        : {'name': 'Backscatter', 'datamax': -3, 'datamin': -8},
        'bSc_TALL'   : {'name': 'Backscatter -- Full Range', 'datamax': -3, 'datamin': -8},
        'snr'        : {'name': 'Intensity', 'datamax': 1.6, 'datamin': 1}
        },
    

    }

file_paths = {

    'dump':{
        'C1':{
            'dlVAD' : f'{plot_base_dir}/clampsdlvadC1',
            'dlfp'  : f'{plot_base_dir}/clampsdlfpC1',
            'aerioe': f'{plot_base_dir}/clampsaerioeC1',
            'tower' : f'{plot_base_dir}/clampstowerC1',
            'mwr'   : f'{plot_base_dir}/clampsmwrC1',
            'housekeeping': f'{plot_base_dir}/clampshousekeepingC1',
            },
        'C2':{
            'dlVAD' : f'{plot_base_dir}/clampsdlvadC2',
            'dlfp'  : f'{plot_base_dir}/clampsdlfpC2',
            'aerioe': f'{plot_base_dir}/clampsaerioeC2',
            'tower' : f'{plot_base_dir}/clampstowerC2',
            'mwr'   : f'{plot_base_dir}/clampsmwrC2',
            'housekeeping': f'{plot_base_dir}/clampshousekeepingC2',
            }
        },

    'data':{
        'C1':{
            'dlVAD' : ['/Users/clamps/data/processed/clampsdlvad1turnC1.c1',
                       '/Users/clamps/data/processed/clampsdlvadC1.c1'],
            'dlfp'  : ['/Users/clamps/data/ingested/clampsdlfpC1.b1'],
            'aerioe': ['/Users/clamps/data/realtime/clampsaerioe1turnC1.c1'],
            'tower' : ['/Users/clamps/data/ingested/clampsmwrC1.a1'], 
            'mwr'   : ['/Users/clamps/data/ingested/clampsmwrC1.a1',
                       '/Users/clamps/data/ingested/clampsmwrC1.a0'], 
            'housekeeping': ['/Users/clamps/data/ingested/clampsaerisummaryC1.b1']
            },
        'C2':{
            'dlVAD' : ['/Users/clamps/data/processed/clampsdlvad1turnC2.c1',
                       '/Users/clamps/data/processed/clampsdlvadC2.c1'],
            'dlfp'  : ['/Users/clamps/data/ingested/clampsdlfpC2.b1'],
            'aerioe': ['/Users/clamps/data/realtime/clampsaerioe1turnC2.c1'],
            'tower' : ['/Users/clamps/data/ingested/clampsmwrC2.a1'],
            'mwr'   : ['/Users/clamps/data/ingested/clampsmwrC2.a1',
                       '/Users/clamps/data/ingested/clampsmwrC2.a0'], 
            'housekeeping': ['/Users/clamps/data/ingested/clampsaerisummaryC2.b1']
            }
        },

    'error_log': '/home/tyler.bell/python/CLAMPS_QL_Plotter/error_log.txt'

    }
