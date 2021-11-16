import get_point_data as gpd
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import os.path

path = os.getcwd()

"""Global Variables"""
ELEM_SIZE = 5e-4
FILE_NAME = []
FRAME_TIME = 300
FINGER_ANGLE = 90 * np.pi / 180
FINGER_VEL = 5e-6


def finger_location(yz, init_pos):
    """Find X position of hot finger surface (offset by 1 element size)"""
    global FINGER_ANGLE, FINGER_VEL, FRAME_TIME
    [y, z] = yz

    if (not -5e-3 <= y <= 5e-3) or (not -10e-3 <= z <= 0):
        print('---WARNING---YZ position outside of domain (ice_front_search: finger_location)')
        quit()

    if z <= -4.5e-3 - ELEM_SIZE or y <= -1.5e-3 - ELEM_SIZE:
        return 10e-3 + init_pos + FRAME_TIME * FINGER_VEL
    else:
        return (-z) / np.tan(FINGER_ANGLE / 2) + init_pos + FRAME_TIME * FINGER_VEL - ELEM_SIZE


def yz_list_generator(y_num, z_num, y_lim=(-4.5e-3, 4.5e-3), z_lim=(-8.5e-3, -0.5e-3)):
    """Generate YZ search gird within range"""
    y_max = min(y_lim[1], 4.5e-3)
    y_min = max(y_lim[0], -4.5e-3)
    z_max = min(z_lim[1], -0.5e-3)
    z_min = max(z_lim[0], -8.5e-3)
    y_list = [round(i * (y_max - y_min) / (y_num - 1) + y_min, 6) for i in range(y_num)]
    z_list = [round(i * (z_max - z_min) / (z_num - 1) + z_min, 6) for i in range(z_num)]

    return y_list, z_list


def yz_search(yz, x_range=(), data_type='temp', info=True, init_pos=10e-3):
    """Search ice front on YZ line using transition temperature"""
    global FILE_NAME, ELEM_SIZE, FRAME_TIME
    [y, z] = yz
    yz_domain = gpd.GetPointData(FILE_NAME, yz, ELEM_SIZE)

    if len(x_range) == 0:
        low = 0
        high = finger_location(yz, init_pos)
    else:
        [low, high] = x_range
        high = min(high, finger_location(yz, init_pos))
    mid = (low + high) / 2

    if data_type == 'temp':
        while True:
            if (high - low) > 1e-9:
                mid = (low + high) / 2
                mid_temp = yz_domain.get_point_data(mid)[1]
                if abs(mid_temp - 273.15) <= 1e-3:
                    break
                elif mid_temp > 273.15:
                    high = mid
                else:
                    low = mid
            else:
                # print('---WARNING---Binary search failed (ice_front_search: yz_search_temp)', FRAME_TIME, yz, mid_temp)
                break

    elif data_type == 'lf':
        while True:
            if (high - low) > 1e-9:
                mid = (low + high) / 2
                mid_lf = yz_domain.get_point_data(mid)[0]
                if 0.0 < mid_lf <= 0.1:
                    break
                elif mid_lf > 0.0:
                    high = mid
                else:
                    low = mid
            else:
                # print('---WARNING---Binary search failed (ice_front_search: yz_search_lf)', FRAME_TIME, yz, mid_lf)
                break
    else:
        print('---WARNING---Incorrect search data type (ice_front_search: yz_search)')
        quit()

    if info:
        return [mid, y, z], yz_domain.get_point_data(mid, info=True)
    else:
        return [mid, y, z]


def grid_search(y_list, z_list, data_type='temp', write=False):
    global FRAME_TIME
    start_time = time.time()
    time_step_data = {}
    i = 0
    print('\n-----Processing Frame:', FRAME_TIME, 's.')
    for y in y_list:
        for z in z_list:
            point, data = yz_search([y, z], data_type=data_type)
            i += 1
            time_step_data[i] = {'position': point, 'liquid_fraction': data[0], 'temperature': data[1]}

    if write:
        with open(os.path.dirname(path) + f'\processed_data\ice_front_{FRAME_TIME}.csv', 'w+') as out_file:
            for key in time_step_data.keys():
                out_file.write("%s,%s\n" % (key, time_step_data[key]))
            out_file.close()

    print('-----Process Time', round(time.time()-start_time, 2), 's.')
    return time_step_data
