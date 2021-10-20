import numpy as np
import matplotlib.pyplot as plt
import os.path
from data_preprocessing import data_preprocess
import cell_average
import get_point_data as gpd


moving_zone = [1e-3 + 10 * 1e-6, 26e-3 + 10 * 1e-6]
a = gpd.GetPointData('FFF-0100', [3.25e-3, -3.25e-3], 0.5e-3, moving_zone)

print("grid num = ",len(a.grid_data))
print("y and z = ", a.y_pos, a.z_pos, "yz_node num = ", len(a.yz_node))
print("1st_node:",a.yz_node[0])
print("2nd_node:",a.yz_node[1])
print("last_node:",a.yz_node[-1])


for i in range(30,31):
    xv = i * 1e-4
    a.get_ice_front_data(xv)
    """anchor_node_index = gpd.anchor_node
    print("x_pos=",xv)
    print("anchor_node=", anchor_node_index, a.yz_node[anchor_node_index])
    print("active_node len = ", len(gpd.active_node))   
    print("1st node: ",gpd.active_node[0],a.grid_data[gpd.active_node[0]])
    print("1st node: ",gpd.active_node[1],a.grid_data[gpd.active_node[1]])
    print("last node: ",gpd.active_node[-1],a.grid_data[gpd.active_node[-1]])
    print("top_index len:", len(gpd.top_index))
    print(gpd.top_index[0], gpd.top_index[1], gpd.top_index[-1])
    print("dis=",gpd.distance[gpd.top_index[0]], gpd.distance[gpd.top_index[1]],gpd.distance[gpd.top_index[2]],gpd.distance[gpd.top_index[3]], gpd.distance[gpd.top_index[-1]])
    print("top_node len=",len(gpd.top_node))
    for node in gpd.top_node:
        print(node, "dis=", cell_average.point_dis(node, np.array([xv, a.y_pos, a.z_pos])) )      
    print("dst pos:", xv, a.y_pos, a.z_pos)
    point = np.array([xv, a.y_pos, a.z_pos])
    p1 = np.array(gpd.top_node[0])
    p2 = np.array(gpd.top_node[1])
    p3 = np.array(gpd.top_node[2])
    p4 = np.array(gpd.top_node[3])
    print(point,p1,p2,p3,p4)
    print(gpd.top_value)
    print("check_closure = ", cell_average.check_closure(point, p1, p2, p3, p4))"""
      
#    for i in range(30, 120):
#        print(a.get_ice_front_data(i*1e-4))

