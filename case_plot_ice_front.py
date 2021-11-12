import json

import numpy as np
import matplotlib.pyplot as plt
import os.path
path = os.getcwd()


print('-----Plot Ice Front-----')


def read_ice_front(file_name):
    with open(file_name, 'r') as in_file:
        ice_front = json.load(in_file)
        in_file.close()
    return ice_front


def plot_pos(ice_front, title, fig_name, vel=True):
    frame_list = []
    x_list = []
    z_list = [-0.0005, -0.0045, -0.0085]
    for key in ice_front:
        frame_list.append(int(key))
        x = ice_front[key][2]

        if len(x) % 2:
            x_list.append([x[0], x[(len(x) - 1) // 2], x[-1]])
        else:
            x_list.append([x[0], (x[len(x)//2] + x[len(x)//2-1])/2, x[-1]])

    plt.figure()
    plt.xlabel('Flow Time (s)')
    plt.ylabel('Ice Front Position (mm)')
    for i, z in enumerate(z_list):
        plt.plot(frame_list, [elem[i] * 1e3 for elem in x_list], '-', label=f'z={z * 1000}mm')
    plt.title(title[0])
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(fig_name[0])
    plt.close()

    if vel:
        vel_frame_list, vel_x_list = [], []
        for i in range(len(x_list) - 1):
            vel_frame_list.append(np.average(frame_list[i:i + 2]))
            vel_x_list.append(
                [(x_list[i + 1][j] - x_list[i][j]) / (frame_list[i+1] - frame_list[i])
                 for j in range(len(z_list))]
            )

        plt.figure()
        plt.xlabel('Flow Time (s)')
        plt.ylabel('Ice Front Velocity (\u03BCm/s)')
        for i, z in enumerate(z_list):
            plt.plot(vel_frame_list, [vel_x_list[j][i] * 1e6 for j in range(len(x_list) - 1)],
                     '-', label=f'z={z * 1000}mm, avg_vel={np.average(vel_x_list[:][i])* 1e6}\u03BCm/s')
        plt.title(title[1])
        # plt.xlim([0, 50])
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(fig_name[1])
        plt.close()

title = [
    f'X Position of Ice Front\n90deg/323.15K hot-finger vel=5\u03BCm/s, y=4.5mm',
    f'X Velocity of Ice Front\n90deg/323.15K hot-finger vel=5\u03BCm/s, y=4.5mm',
]
fig_name = [
    os.path.dirname(path) + f'/images/11-06-2021/90deg-5vel-video-2000/x position',
    os.path.dirname(path) + f'/images/11-06-2021/90deg-5vel-video-2000/x velocity'
]
file_name = os.path.dirname(path) + f'/images/11-06-2021/90deg-5vel-video-2000/data.txt'

ice_front = read_ice_front(file_name)
plot_pos(ice_front, title, fig_name)

print('-----Plot Ice Front END-----')
