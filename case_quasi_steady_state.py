import numpy as np
import ice_front_search as ifs
from tqdm import trange
import matplotlib.pyplot as plt


print('-----Quasi Steady State Determination-----')


def plot(end_time, y):
    n = 30
    frame_list = np.logspace(np.log10(10), np.log10(end_time), dtype=int, num=n)
    frame_list = sorted(set(frame_list))
    frame_num = len(frame_list)

    x = []
    z_list = [-0.5e-3, -4.5e-3, -8.5e-3]
    finger_vel = 5e-6
    ifs.ELEM_SIZE = 0.3e-3

    for i in range(frame_num):
        ifs.FILE_NAME = ['0.3mesh/center-' + str(frame_list[i]) + '.0']
        ifs.FRAME_TIME = frame_list[i]
        x_frame = []
        for z in z_list:
            # temp_y0 = ifs.yz_search((y, z), info=False)
            x_frame.append(ifs.yz_search((y, z), info=False)[0] - frame_list[i] * finger_vel - 3e-3)
        x.append(x_frame)

    vel_frame_list, vel_x_list = [], []
    for i in range(frame_num-1):
        vel_frame_list.append(np.average(frame_list[i:i+2]))
        vel_x_list.append([(x[i+1][j]-x[i][j])/vel_frame_list[i] + finger_vel for j in range(len(z_list))])

    plt.figure()
    # Ice front position
    plt.xlabel('Flow Time (s)')
    plt.ylabel('Relative Ice Front Position (mm)')
    for i, z in enumerate(z_list):
        plt.plot(frame_list, [x[j][i]*1e3 for j in range(frame_num)], '.-', label=f'z={z*1000}mm')
    plt.title(f'X Position of Ice Front Relative to Hot-finger Tip'
              f'\n90deg/323.15K hot-finger, 0.3mm mesh, y={y*1000}mm')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'images/if_pos_0.3mesh_y{y}_{end_time}.png')
    plt.close()

    plt.figure()
    # Ice front velocity
    plt.xlabel('Flow Time (s)')
    plt.ylabel('Ice Front Velocity (\u03BCm/s)')
    for i, z in enumerate(z_list):
        plt.plot(vel_frame_list, [vel_x_list[j][i]*1e6 for j in range(frame_num-1)], '.-', label=f'z={z * 1000}mm')
    plt.title(f'Velocity of Ice Front Propagation along X-axis'
              f'\n90deg/323.15K hot-finger, 0.3mm mesh, y={y * 1000}mm')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(f'images/if_vel_0.3mesh_y{y}_{end_time}.png')
    plt.close()


plot(250, 0e-3)
print('-----Quasi Steady State END-----')
