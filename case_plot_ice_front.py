import json
import ice_front_search as ifs
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


def plot_pos(ice_front, title, fig_name, z_list, vel=True):
    frame_list = []
    x_list = []
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
            vel_list = [vel_x_list[j][i] * 1e6 for j in range(len(x_list) - 1)]
            plt.plot(vel_frame_list, vel_list,
                     '-', label=f'z={z * 1000}mm, avg_vel={round(np.average(vel_list), 3)}\u03BCm/s')
        plt.title(title[1])
        # plt.xlim([0, 50])
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig(fig_name[1])
        plt.close()


def y_plane_gradient():
    print('\n-----Y Plane gradient test-----')
    ifs.ELEM_SIZE = 0.5e-3
    ifs.FRAME_TIME = 700
    ifs.FILE_NAME = ['/11-15-2021 sync cold source 5/center-700.0']

    n = 10
    y_list, z_list = ifs.yz_list_generator(n, n, z_lim=(-6e-3, -1e-3))
    temp_y0 = ifs.grid_search([0], z_list, data_type='temp')

    x, y, z = [], [], []
    grad_x, grad_y, grad_z = [], [], []
    for key in temp_y0:
        x.append(temp_y0[key]['position'][0] * 1000)
        y.append(temp_y0[key]['position'][1] * 1000)
        z.append(temp_y0[key]['position'][2] * 1000)
        grad_x.append(temp_y0[key]['temperature'][1][0])
        grad_y.append(temp_y0[key]['temperature'][1][1])
        grad_z.append(temp_y0[key]['temperature'][1][2])

    plt.figure(figsize=(6, 6))

    color1 = 'tab:blue'
    color2 = 'tab:red'
    plt.xlabel('X Position (mm)')
    plt.ylabel('Z Position (mm)')
    plt.plot(x, z, color=color1)
    plt.xlim(10, 3)
    plt.axis('equal')

    norm_factor = 3 / max(grad_x)
    print(max(grad_x))
    scale = int(max(grad_x)/3*2)
    for i in range(n):
        arrow_x = grad_x[i] * norm_factor
        arrow_z = grad_z[i] * norm_factor
        plt.arrow(x[i], z[i], arrow_x, arrow_z,
                  head_width=0.1, head_length=0.2, length_includes_head=True,
                  color=color2)

    plt.text(13, -5.7, f'{scale} K/m', fontsize=12, horizontalalignment='center')
    plt.arrow(12, -6, 2, 0, head_width=0.1, head_length=0.2, length_includes_head=True, color=color2)
    plt.title(f'Temperature Gradient (projected on XZ plane) at Ice Front'
              f'\nvel = 5\u03BCm/s, y = 0 mm, t = {ifs.FRAME_TIME}s')
    plt.tight_layout()

    plt.savefig(os.path.dirname(path) + '/images/11-15-2021/reduced domain 5/gradient')
    plt.close()

    print('-----Y Plane gradient test END-----')


# title = [
#     f'X Position of Ice Front\n90deg/323.15K hot-finger vel=5\u03BCm/s, y=0mm',
#     f'X Velocity of Ice Front\n90deg/323.15K hot-finger vel=5\u03BCm/s, y=0mm',
# ]
# fig_name = [
#     os.path.dirname(path) + f'/images/11-15-2021/reduced domain 5/x position',
#     os.path.dirname(path) + f'/images/11-15-2021/reduced domain 5/x velocity'
# ]
# file_name = os.path.dirname(path) + f'/images/11-15-2021/reduced domain 5/data.txt'
# z_list = [-1e-3, -3e-3, -6e-3]
#
# ice_front = read_ice_front(file_name)
# plot_pos(ice_front, title, fig_name, z_list)

y_plane_gradient()

print('-----Plot Ice Front END-----')
