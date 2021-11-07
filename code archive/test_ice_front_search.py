import ice_front_search as ifs
from tqdm import trange
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar

# print('\n-----finger location test-----')
# for i in range(9):
#     yz = [0, -9e-3/9 * i]
#     print(yz, ifs.finger_location(yz))
# for i in range(10):
#     yz = [-5e-3 + 10e-3/10*(i+1), 0]
#     print(yz, ifs.finger_location(yz))
# print('-----finger location test END-----')


# print('\n-----YZ search test-----')
# for i in range(7):
#     yz = [0, -1e-3 * (i + 1)]
#     print(yz, ifs.yz_search_temp(yz)[1])

# for i in range(9):
#     yz = [-1e-3 * (i - 4), -4.5e-3]
#     print(yz, ifs.yz_search_temp(yz))

# for i in range(7):
#     yz = [0, -1e-3 * (i + 1)]
#     a = ifs.yz_search(yz)
#     print('---', yz, a[0])
#     print(a[1][0])
#     print(a[1][1])
#
# for i in range(9):
#     yz = [-1e-3 * (i - 4), -4.5e-3]
#     a = ifs.yz_search(yz)
#     print('---', yz, a[0])
#     print(a[1][0])
#     print(a[1][1])
# print('-----YZ search test END-----')


# print('\n-----List generator test-----')
# print(ifs.yz_list_generator(11, 21))
# print(ifs.yz_list_generator(11, 21, [2e-3, 3e-3], [-6e-3, -2e-3]))
# print('-----List generator test END-----')


def y_plane_search():
    print('\n-----Y Plane search test-----')
    ifs.ELEM_SIZE = 0.3e-3
    n = 30
    frames = [50, 100, 150, 200, 250]
    x_if_pos, z_if_pos = [], []

    for frame_time in frames:
        ifs.ELEM_SIZE = 0.3e-3
        ifs.FRAME_TIME = frame_time
        ifs.FILE_NAME = [f'0.3mesh/center-{frame_time}.0']
        y_list, z_list = ifs.yz_list_generator(n, n)
        temp_y0 = ifs.grid_search([0], z_list, data_type='temp')

        temp_x, temp_z = [], []
        for key in temp_y0:
            temp_x.append(temp_y0[key]['position'][0] * 1000)
            temp_z.append(temp_y0[key]['position'][2] * 1000)
        x_if_pos.append(temp_x)
        z_if_pos.append(temp_z)

    # Plot
    plt.figure(figsize=(7.5, 7.5))

    plt.xlim(10, 3)
    plt.xlabel('X Position (mm)')
    plt.ylabel('Z Position (mm)')
    for i, frame_time in enumerate(frames):
        plt.plot(x_if_pos[i], z_if_pos[i], label=f'time={frame_time}s')
    plt.legend(loc="upper left")

    plt.axis('equal')
    plt.title('Ice Front Position on XZ Mid-plane'
              '\n90deg/323.15K hot-finger, y = 0 mm')
    plt.tight_layout()

    plt.savefig('images/y=0 ice_front multi.png', bbox_inches='tight')
    plt.close()

    print('-----Y Plane search test END-----')


def z_plane_search():
    print('\n-----Z Plane search test-----')
    y_list, z_list = ifs.yz_list_generator(50, 50)
    temp_z = ifs.grid_search(y_list, [-4.5e-3], data_type='temp')
    lf_z = ifs.grid_search(y_list, [-4.5e-3], data_type='lf')

    temp_x, temp_y = [], []
    lf_x, lf_y = [], []
    for key in temp_z:
        temp_x.append(temp_z[key]['position'][0] * 1000)
        temp_y.append(temp_z[key]['position'][1] * 1000)
        lf_x.append(lf_z[key]['position'][0] * 1000)
        lf_y.append(lf_z[key]['position'][1] * 1000)
        # print(temp_y0[key]['position'])
    # print(temp_x, temp_y)
    # print(lf_x, lf_y)
    fig, ax = plt.subplots()

    color1 = 'tab:blue'
    color2 = 'tab:red'
    ax.set_xlim(8.5, 6)
    ax.set_xlabel('X Position (mm)')
    ax.set_ylabel('Y Position (mm)')
    ax.plot(temp_x, temp_y, color=color2, label='Temperature')
    ax.plot(lf_x, lf_y, color=color1, label='Liquid Fraction')
    ax.legend(loc="upper left")

    plt.title('90deg/323.15K hot-finger, z = -4.5 mm, t = 300s')
    fig.tight_layout()

    plt.savefig('images/z-4.5_if_temp_lf.png')
    plt.close()

    print('-----Z Plane search test END-----')


def y_plane_gradient():
    print('\n-----Y Plane gradient test-----')
    ifs.ELEM_SIZE = 0.2e-3
    ifs.FRAME_TIME = 250
    ifs.FILE_NAME = ['0.2mesh/center-250.0']

    n = 40
    y_list, z_list = ifs.yz_list_generator(n, n)
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

    # print('X position:', x)
    # print('Y position:', y)
    # print('Z position:', z)
    # print('X gradient:', grad_x)
    # print('Y gradient:', grad_y)
    # print('Z gradient:', grad_z)

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
    # plt.text(10, 0, 'Liquid Slurry\nRegion', fontsize=12)
    # plt.text(5, -4, 'Solid Slurry\nRegion', fontsize=12)
    plt.text(4, -7.7, f'{scale} K/m', fontsize=12, horizontalalignment='center')
    plt.arrow(3, -8, 2, 0, head_width=0.1, head_length=0.2, length_includes_head=True, color=color2)
    plt.title('Temperature Gradient (projected on XZ plane) at Ice Front'
              '\n90deg/323.15K hot-finger, y = 0 mm, t = 250s')
    plt.tight_layout()

    plt.savefig('images/y0_if_grad_2ElemSize.png')
    plt.close()

    print('-----Y Plane gradient test END-----')


# y_plane_search()
y_plane_gradient()