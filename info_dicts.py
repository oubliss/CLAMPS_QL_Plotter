# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 18:56:36 2021

@author: Marshall
"""

data_info = {
    
    'dlVAD' : {
        'wSpd'    : {'name': 'Wind Speed', 'datamax':30,  'datamin':0},
        'wDir'    : {'name': 'Wind Direction', 'datamax':360, 'datamin':0}
        },
    
    'dlfp'  : {
        'w_ls'       : {'name': 'Vertical Velocity (High Sensitivity)', 'datamax': 2, 'datamin': -2},
        'w_hs'       : {'name': 'Vertical Velocity (Low Sensitivity)', 'datamax': 5, 'datamin': -5},
        'bSc'        : {'name': 'Backscatter', 'datamax': -3, 'datamin': -8},
        'bSc_TALL'   : {'name': 'Backscatter -- Full Range', 'datamax': -3, 'datamin': -8},
        'snr'        : {'name': 'Intensity', 'datamax': 1.6, 'datamin': 1}
        },
    
    'aerioe': {
        'ptemp'      : {'name': 'Potential Temperature', 'datamax': None, 'datamin': None},
        'temp'       : {'name': 'Temperature', 'datamax': None, 'datamin': None},
        'dewpt'      : {'name': 'Dewpoint', 'datamax': None, 'datamin': None},
        }
    }

file_paths = {
    
    'dump':{
        'C1':{
            'dlVAD' : '/data/mbaldwin/visualizations/clampsdlvadC1',
            'dlfp'  : '/data/mbaldwin/visualizations/clampsdlfpC1',
            'aerioe': '/data/mbaldwin/visualizations/clampsaerioeC1'
            },
        'C2':{
            'dlVAD' : '/data/mbaldwin/visualizations/clampsdlvadC2',
            'dlfp'  : '/data/mbaldwin/visualizations/clampsdlfpC2',
            'aerioe': '/data/mbaldwin/visualizations/clampsaerioeC2'
            }
        },
    
    'data':{
        'C1':{
            'dlVAD' : ['/data/clamps/clamps1/processed/clampsdlvad1turnC1.c1',
                       '/data/clamps/clamps1/processed/clampsdlvadC1.c1'],
            'dlfp'  : ['/data/clamps/clamps1/ingested/clampsdlfpC1.b1'],
            'aerioe': ['/data/clamps/clamps1/realtime/clampsaerioe1turnC1.c1']
            },
        'C2':{
            'dlVAD' : ['/data/clamps/clamps2/processed/clampsdlvad1turnC2.c1',
                       '/data/clamps/clamps2/processed/clampsdlvadC2.c1'],
            'dlfp'  : ['/data/clamps/clamps2/ingested/clampsdlfpC2.b1/clampsdlfpC2.b1'],
            'aerioe': ['/data/clamps/clamps2/realtime/clampsaerioe1turnC2.c1']
            }
        },
    
    'error_log': '/data/mbaldwin/visualizations/error_log/error_log.txt'
    
    }