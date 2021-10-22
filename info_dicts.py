# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 18:56:36 2021

@author: Marshall
"""

valid_filename_info = {
    
    'dlVAD': {'file_length': [41, 36]},
    'dlfp' : {'file_length': 35}
    
    }

data_info = {
    
    'dlVAD' : {
        'wSpd'    : {'name': 'Wind Speed', 'datamax':30,  'datamin':0},
        'wDir'    : {'name': 'Wind Direction', 'datamax':360, 'datamin':0}
        },
    
    'dlfp'  : {
        'w'       : {'name': 'Vertical Velocity', 'datamax': 5, 'datamin': -5},
        'ws'      : {'name': 'Horizontal Wind Speed', 'datamax': None, 'datamin': None},
        'wd'      : {'name': 'Horizontal Wind Direction', 'datamax': None, 'datamin': None},
        'pt'      : {'name': 'Potential Temperature', 'datamax': None, 'datamin': None},
        't'       : {'name': 'Temperature', 'datamax': None, 'datamin': None},
        'q'       : {'name': 'Specific Humidity', 'datamax': None, 'datamin': None},
        'dp'      : {'name': 'Dewpoint', 'datamax': None, 'datamin': None},
        'rh'      : {'name': 'Relative Humidity', 'datamax': None, 'datamin': None},
        'std'     : {'name': 'Standard Deviation', 'datamax': None, 'datamin': None},
        'bSc'     : {'name': 'Backscatter', 'datamax': -3, 'datamin': -8},
        'bSc_TALL': {'name': 'Backscatter -- Full Range', 'datamax': -3, 'datamin': -8},
        'snr'     : {'name': 'Intensity', 'datamax': 1.6, 'datamin': 1}
        }
    }

file_paths = {
    
    'dump':{
        'C1':{
            'dlVAD' : '/data/mbaldwin/visualizations/clampsdlvadC1.c1',
            'dlfp'  : '/data/clamps/clamps1/ingested/clampsdlfpC1.b1'
            }
        },
    
    'data':{
        'C1':{
            'dlVAD' : ['/data/clamps/clamps1/processed/clampsdlvad1turnC1.c1',
                       '/data/clamps/clamps1/processed/clampsdlvadC1.c1'],
            'dlfp' : '/data/clamps/clamps1/ingested/clampsdlfpC1.b1'
            }    
        }
    }