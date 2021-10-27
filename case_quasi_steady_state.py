import ice_front_search as ifs
import numpy as np
import matplotlib.pyplot as plt


print('-----Quasi Steady State Determination-----')

frame_num = 3
frame_list = [int(600 / frame_num * (i+1)) for i in range(frame_num)]
frame_list.insert(0, 1)
print('Frame List:', frame_list)

x = []
y = 0
z_list = [-2.25e-3, -4.5e-3, -6.75e-3]
finger_vel = 5e-3  # mm/s

for i in range(frame_num):
    ifs.FILE_NAME = ['center-' + str(frame_list[i]).zfill(4)]
    ifs.FRAME_TIME = frame_list[i]
    print(ifs.FILE_NAME)
    x_frame = []
    for z in z_list:
        temp_y0 = ifs.yz_search((y, z), info=False)
        x_frame.append(ifs.yz_search((y, z), info=False)[0] - frame_list[i] * finger_vel)  # mm
    x.append(x_frame)

fig, ax = plt.figure()

color = ['tab:blue', 'tab:red', 'tab:']
ax.set_xlabel('Relative X Position (mm)')
ax.set_ylabel('Z Position (mm)')
for i, z in enumerate(z_list):
    ax.plot(frame_list, x[i], label=f'z = {z}mm')

plt.title('90deg/323.15K hot-finger, y = 1.75 mm')
fig.tight_layout()

plt.savefig('images/if_trajectory.png')
plt.close()

print('-----Quasi Steady State END-----')
