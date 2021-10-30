import numpy as np
import ice_front_search as ifs
from tqdm import trange
import matplotlib.pyplot as plt


print('-----Quasi Steady State Determination-----')


def plot(end_time, y):
    frame_list = np.logspace(np.log10(20), np.log10(end_time), dtype=int, num=30)
    frame_list = sorted(set(frame_list))
    frame_num = len(frame_list)

    x = []
    z_list = [-1e-3, -4.5e-3, -8e-3]
    finger_vel = 5e-6  # mm/s

    for i in range(frame_num):
        ifs.FILE_NAME = ['center-' + str(frame_list[i]).zfill(4)]
        ifs.FRAME_TIME = frame_list[i]
        x_frame = []
        for z in z_list:
            temp_y0 = ifs.yz_search((y, z), info=False)
            x_frame.append(ifs.yz_search((y, z), info=False)[0] - frame_list[i] * finger_vel)  # mm
        x.append(x_frame)

    # frame_list.insert(0, 0)
    # x.insert(0, [0, 0, 0])

    plt.figure()

    color = ['tab:blue', 'tab:red', 'tab:']
    plt.xlabel('Flow Time (s)')
    plt.ylabel('Relative X Position (mm)')
    for i, z in enumerate(z_list):
        plt.plot(frame_list, [x[j][i] for j in range(frame_num)], '.-', label=f'z={z*1000}mm')

    plt.title(f'90deg/323.15K hot-finger, 0.5mm mesh, y={y*1000}mm')
    plt.legend(loc='lower right')
    # plt.tight_layout()

    plt.savefig(f'images/2_if_trajectory_0.5mesh_y{y}_{end_time}.png')
    plt.close()


plot(600, -1.5e-3)
plot(600, 4.5e-3)
# plot(200, 0.0)
# plot(200, 3.5e-3)
print('-----Quasi Steady State END-----')
