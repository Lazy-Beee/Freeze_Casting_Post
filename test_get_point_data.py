import numpy as np

import data_preprocessing as dp
import get_point_data as gpd
import matplotlib.pyplot as plt
from tqdm import trange


FILE_NAME = ['center-0300', 'node-0300']
ELEM_SIZE = 5e-4
x = 0.005
y = 0.000
z = -0.008

# node_data = dp.data_preprocess(file_name)
# print('\n-----Data Processing Test-----')
# print(f'Data length: {len(node_data)}')
# print(node_data[1])
# print(node_data[len(node_data)])
# print('-----Data Processing Test-----')

a = gpd.GetPointData(FILE_NAME, [y, z], ELEM_SIZE)
# print('\n-----Tetrahedron search Test-----')
# active_node = a.get_active_node(x)
# print('---Number of node within search range:', len(active_node), '. Node index:')
# print(active_node)
# a.get_tet_node(x, y, z, active_node)
#
n = 100
x_pos = []
result = []
lf = []
temp = []
for i in trange(n):
    start = 0.0082
    end = 0.0095
    x_pos.append(start + i * (end - start) / (n - 1))
    result.append(a.get_ice_front_data(x_pos[-1]))
    lf.append(result[-1][0])
    temp.append(result[-1][1])
#     print('%.6f' % x_pos[-1], result[-1])
# print(a.get_ice_front_data(0.0069, info=True))
#
# print('-----Tetrahedron search Test END-----')

"""Plot x-axis search"""
x_pos = np.array(x_pos) * 1000

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('X Position (mm)')
ax1.set_ylabel('Liquid Fraction', color=color)
ax1.plot(x_pos, lf, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Temperature (K)', color=color)
ax2.plot(x_pos, temp, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('90deg/323.15K hot-finger, (y,z) = (0,-8) mm, t = 300s')
fig.tight_layout()

plt.savefig('images/y0_z-8.png')
plt.close()
