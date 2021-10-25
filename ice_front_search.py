import get_point_data as gpd
import matplotlib.pyplot as plt
import numpy as np

"""Global Variables"""
ELEM_SIZE = 5e-4
FILE_NAME = ['center-0300', 'node-0300']
RUNTIME = 300
FINGER_ANGLE = 90 * np.pi / 180
FINGER_VEL = 5e-6


def finger_location(yz):
    """Find X position of hot finger surface (offset by 1 element size)"""
    global FINGER_ANGLE, FINGER_VEL, RUNTIME
    [y, z] = yz

    if (not -1.5e-3 <= y <= 5e-3) or (not -9e-3 <= z <= 0):
        print('---WARNING---YZ position outside of domain (ice_front_search: finger_location)')
        quit()

    if z <= -4e-3 - ELEM_SIZE:
        return 12e-3 + 3e-3 + RUNTIME * FINGER_VEL
    else:
        return (-z) / np.tan(FINGER_ANGLE / 2) + 3e-3 + RUNTIME * FINGER_VEL - ELEM_SIZE


def yz_search_temp(yz, x_range=()):
    """Search ice front on YZ line using transition temperature"""
    global FILE_NAME, ELEM_SIZE
    [y, z] = yz
    yz_domain = gpd.GetPointData(FILE_NAME, yz, ELEM_SIZE)

    if len(x_range) == 0:
        low = 0
        high = finger_location(yz)
    else:
        [low, high] = x_range
        high = min(high, finger_location(yz))

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
            print('---WARNING---Binary search failed (ice_front_search: yz_search_temp)')
            return None

    return [mid, y, z], yz_domain.get_point_data(mid, info=True)


def yz_search_lf(yz, x_range):
    """Search ice front on YZ line"""
    global FILE_NAME, ELEM_SIZE
    [y, z] = yz
    yz_domain = gpd.GetPointData(FILE_NAME, yz, ELEM_SIZE)

    if len(x_range) == 0:
        low = 0
        high = finger_location(yz)
    else:
        [low, high] = x_range
        high = min(high, finger_location(yz))

    while True:
        if (high - low) > 1e-9:
            mid = (low + high) / 2
            mid_lf = yz_domain.get_point_data(mid)[0]
            if 0.0 < mid_lf <= 0.2:
                break
            elif mid_lf > 0.0:
                high = mid
            else:
                low = mid
        else:
            print('---WARNING---Binary search failed (ice_front_search: yz_search_lf)')
            return None

    return [mid, y, z], yz_domain.get_point_data(mid, info=True)
