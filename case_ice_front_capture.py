import cv2
import numpy as np
import ice_front_search as ifs
import matplotlib.pyplot as plt
import json
import os.path
path = os.getcwd()


print('-----Ice Front Capture-----')


def get_ice_front(frame_list, n, y):
    frame_num = len(frame_list)
    z_list = [-0.5e-3 - i * 8e-3 / (n-1) for i in range(n)]
    y_list = [y]
    ifs.FINGER_VEL = 5e-6
    ifs.ELEM_SIZE = 0.3e-3

    ice_front = []
    for i in range(frame_num):
        print(f'---Processing Frame: {frame_list[i]}---')
        ifs.FILE_NAME = ['03 90deg-50C-5 data/center-' + str(frame_list[i]) + '.0']
        ifs.FRAME_TIME = frame_list[i]
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

        fig = plt.figure(figsize=(6, 12))
        plt.axis('equal')
        plt.ylim(0, 15)
        plt.xlabel('Z Position (mm)')
        plt.ylabel('X Position (mm)')
        plt.plot(z_if_pos*1000, x_if_pos*1000)
        plt.text(-4.5, 15, f'time={frame_time}s', fontsize=12, horizontalalignment='center')
        plt.gca().set_aspect('equal')
        plt.title(title)
        plt.savefig(os.path.dirname(path) + f'{file_path}\\{i}')
        plt.close()


def gen_video(file_path, frame_num):
    img_array = []
    for i in range(frame_num):
        img = cv2.imread(f'{file_path}/{i}.png')
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(os.path.dirname(path) + f'{file_path}/video.avi',
                          cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def write_ice_front(ice_front, file_name):
    dic = {}
    for frame in ice_front:
        dic[frame[0]] = [frame[1], frame[2], frame[3]]
    with open(f'{file_name}.txt', 'w+') as out_file:
        json.dump(dic, out_file)
        out_file.close()


# def read_ice_front(file_name):
#     ice_front = {}
#     with open(f'data storage/{file_name}.txt', 'r') as in_file:
#         reader = csv.reader(in_file)
#         for row in reader:
#             print(row)
#             ice_front[row[0]](row[1])
#         in_file.close()
#     return ice_front


# frame_list = np.logspace(np.log10(5), np.log10(180), dtype=int, num=3)
# frame_list = sorted(set(frame_list))
# frame_num = len(frame_list)

frame_num = 201
frame_list = [180 + i*10 for i in range(frame_num)]

ice_front = get_ice_front(frame_list, 10, 4.5e-3)
file_path = 'images/11-06-2021/90deg-5vel-video-2000'
video_title = 'Ice Front Position Close to Slurry Surface\n90deg/323.15K, hot-finger vel=5um/s, y=4.5mm'
prep_video(ice_front, file_path, video_title)
gen_video(file_path, frame_num)
write_ice_front(ice_front, f'{file_path}/data')

print('-----Ice Front Capture END-----')
