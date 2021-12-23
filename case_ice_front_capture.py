import cv2
import numpy as np
import ice_front_search as ifs
import matplotlib.pyplot as plt
import json
from tqdm import trange
import os.path
path = os.getcwd()


def get_ice_front(frame_list, y, start_time, init_pos, data_file_name, z_list):
    frame_num = len(frame_list)
    y_list = [y]
    ifs.FINGER_VEL = 5e-6
    ifs.ELEM_SIZE = 0.5e-3
    ifs.MOTION_START_TIME = start_time

    ice_front = []
    for i in trange(frame_num):
        ifs.FILE_NAME = [data_file_name + str(frame_list[i]) + '.0']
        ifs.FRAME_TIME = frame_list[i]  # Pay attention to flow time.
        x_frame = []
        for z in z_list:
            x_frame.append(ifs.yz_search((y, z), info=False, init_pos=init_pos)[0])
        ice_front.append([int(frame_list[i]), y_list, z_list, x_frame])

    return ice_front


def prep_video(ice_front, file_path, title):
    for i in np.arange(len(ice_front)):
        frame_time = ice_front[i][0]
        x_if_pos = np.array(ice_front[i][3])
        z_if_pos = np.array(ice_front[i][2])

        plt.figure(figsize=(6, 12))
        plt.axis('equal')
        plt.ylim(0, 15)
        plt.xlabel('Z Position (mm)')
        plt.ylabel('X Position (mm)')
        plt.plot(z_if_pos*1000, x_if_pos*1000)
        plt.text(-4.5, 13, f'time={frame_time}s', fontsize=12, horizontalalignment='center')
        plt.gca().set_aspect('equal')
        plt.title(title)
        plt.savefig(os.path.dirname(path) + f'/{file_path}/{i}')
        plt.close()


def gen_video(file_path, frame_num):
    img_array = []
    for i in range(frame_num):
        img = cv2.imread(os.path.dirname(path) + f'/{file_path}/{i}.png')
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(os.path.dirname(path) + f'/{file_path}/video.avi',
                          cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def multi_if(ice_front, file_path):
    plt.figure(figsize=(10, 7.5))

    plt.xlim(10, 3)
    plt.xlabel('X Position (mm)')
    plt.ylabel('Z Position (mm)')
    for frame in ice_front:
        plt.plot([x*1000 for x in frame[3]], [x*1000 for x in frame[2]], label=f'time={frame[0]}s')
    plt.legend(bbox_to_anchor=(1.04,1), loc='upper left')

    plt.axis('equal')
    plt.title('Ice Front Position on XZ plane, y = -0.5 mm')
    plt.tight_layout()

    plt.savefig(os.path.dirname(path) + f'/{file_path}/multi ice front', bbox_inches='tight')
    plt.close()


def write_ice_front(ice_front, file_name):
    dic = {}
    for frame in ice_front:
        dic[frame[0]] = [frame[1], frame[2], frame[3]]
    with open(file_name, 'w+') as out_file:
        json.dump(dic, out_file)
        out_file.close()


def read_ice_front(file_name):
    ice_front = []
    with open(file_name, 'r') as in_file:
        data = json.load(in_file)
        in_file.close()
    for key in data:
        ice_front.append([int(key), data[key][:]])
    return ice_front


'''Operation'''
# frame_list = np.logspace(np.log10(5), np.log10(180), dtype=int, num=3)
# frame_list = sorted(set(frame_list))
# frame_num = len(frame_list)

# frame_num = 55
# start_frame = 1
# end_frame = 162
# step_size = (end_frame - start_frame) // (frame_num - 1)
# frame_list = [start_frame + i*step_size for i in range(frame_num)]

start_frame = 300
end_frame = 1300
step_size = 200
frame_list = []
current_frame = start_frame
while current_frame <= end_frame:
    frame_list.append(current_frame)
    current_frame += step_size

frame_list = [300, 500, 700, 900, 1100, 1300, 1495, 1695, 1895, 2095, 2295]

# z_list = [-1.31e-3, -2.62e-3, -3.93e-3, -5.24e-3, -7.86e-3]
# z_list = [-7.846e-3/8*(i+1) for i in range(8)]
z_list = ifs.yz_list_generator(2, 20, z_lim=(-7.5e-3, -0.5e-3))[1]

data_file_name = '12-22-2021 90deg 8mm/center-'
file_path = 'images/12-23-2021'
video_title = 'Ice Front Position Close to Slurry Surface\n90deg, hot-finger vel=5\u03BCm/s, y=4.5mm'

y_pos = -0.5e-3
start_time = 300
init_pos = 3e-3
ice_front = get_ice_front(frame_list, y_pos, start_time, init_pos, data_file_name, z_list)
write_ice_front(ice_front, os.path.dirname(path) + f'/{file_path}/data.txt')
# prep_video(ice_front, file_path, video_title)
# gen_video(file_path, frame_num)
multi_if(ice_front, file_path)

