import cv2
import numpy as np
import ice_front_search as ifs
import matplotlib.pyplot as plt
import json
from tqdm import trange
import os.path
path = os.getcwd()


print('-----Ice Front Capture-----')


def get_ice_front(frame_list, n, y, start_time, data_file_name, z_list):
    frame_num = len(frame_list)
    # z_list = [-0.5e-3 - i * 8e-3 / (n-1) for i in range(n)]
    y_list = [y]
    ifs.FINGER_VEL = 4.5e-6
    ifs.ELEM_SIZE = 0.3e-3

    ice_front = []
    for i in trange(frame_num):
        ifs.FILE_NAME = [data_file_name + str(frame_list[i]) + '.0']
        ifs.FRAME_TIME = frame_list[i] - start_time  # Pay attention to flow time.
        x_frame = []
        for z in z_list:
            x_frame.append(ifs.yz_search((y, z), info=False)[0])
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
        plt.text(-4.5, 15, f'time={frame_time}s', fontsize=12, horizontalalignment='center')
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


# frame_list = np.logspace(np.log10(5), np.log10(180), dtype=int, num=3)
# frame_list = sorted(set(frame_list))
# frame_num = len(frame_list)

# frame_num = 55
# start_frame = 1
# end_frame = 162
# step_size = (end_frame - start_frame) // (frame_num - 1)
# frame_list = [start_frame + i*step_size for i in range(frame_num)]

start_frame = 5
end_frame = 162
step_size = 5
frame_list = []
current_frame = start_frame
while current_frame <= end_frame:
    frame_list.append(current_frame)
    current_frame += step_size

z_list = [-0.5e-3, -2.32e-3, -4.65e-3, -6.97e-3, -9.30e-3]
data_file_name = '11-11-2021-90-05-162 -30cp\\center-'
file_path = 'images\\11-11-2021\\90-5-162-30cp'
video_title = 'Ice Front Position Close to Slurry Surface\n90deg/323.15K, hot-finger vel=5\u03BCm/s, y=4.5mm'
ice_front = get_ice_front(frame_list, 11, 4.5e-3, 180, data_file_name, z_list)
write_ice_front(ice_front, os.path.dirname(path) + f'/{file_path}/data.txt')
prep_video(ice_front, file_path, video_title)
# gen_video(file_path, frame_num)

print('-----Ice Front Capture END-----')
