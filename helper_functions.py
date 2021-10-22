# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:44:41 2021

@author: Marshall
"""
import numpy as np
from datetime import datetime

def uv_from_spd_dir(speed, wdir):
    wdir = np.deg2rad(wdir)
    u = -speed * np.sin(wdir)
    v = -speed * np.cos(wdir)
    return u, v

def get_QL_name(facility,file_type, data_type, date):
    
    date_format = "%Y%m%d"
    date_str = datetime.strftime(date, date_format)
    
    name = f"QL.{facility}.{file_type}.{data_type}.{date_str}.png"
    
    return name