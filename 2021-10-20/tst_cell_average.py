import numpy as np
import matplotlib.pyplot as plt
import os.path
from data_preprocessing import data_preprocess
import cell_average
import math


# test for cell_average



"""def plane_from_3_points(p1, p2, p3):"""
"""Find plane equation ax+by+cd+d=0, return [a,b,c,d]"""
"""a = (p2[1] - p1[1]) * (p3[2] - p1[2]) - (p3[1] - p1[1]) * (p2[2] - p1[2])
    b = (p2[2] - p1[2]) * (p3[0] - p1[0]) - (p3[2] - p1[2]) * (p2[0] - p1[0])
    c = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    d = - (a * p1[0] + b * p1[1] + c * p1[2])
    return [a, b, c, d]"""
def tst_plane_res(abcd,p):
    return abcd[0]*p[0]+abcd[1]*p[1]+abcd[2]*p[2]+abcd[3]
print("########test plane_from_3_points")   
p1 = [-2.0, 1.0, 2.0]
p2 = [3.1,  4.5, 5.6]
p3 = [-0.2, 7.1, 10.8]
abcd = cell_average.plane_from_3_points(p1,p2,p3)
print("abcd=", abcd)
print("(need = 0) ", tst_plane_res(abcd,p1))
print("(need = 0) ", tst_plane_res(abcd,p2))
print("(need = 0) ", tst_plane_res(abcd,p3))
print("")



"""def dis_point_to_plane(point, plane):
    """"""Find distance (directional) form point to plane"""
"""    [x, y, z] = point
    [a, b, c, d] = plane
    return (a*x+b*y+c*z+d)/np.linalg.norm([a, b, c])
"""
print("########test dis_point_to_plane")
ps = [[1,2,3],[-15,-20,-25]]
planes = [[1,0,0,1], [0,1,0,2], [0,0,1,3]]
for p in ps:
    for plane in planes:
        print(p, plane,"dis=", cell_average.dis_point_to_plane(p, plane))
print("")


    
"""def point_dis(p1, p2):
    Distance between two points
    return np.linalg.norm(p1 - p2)"""
print("########test point_dis")
p1s = [[1,2,3],[0,0,0],[3,4,5]]
p2s = [[2,3,4],[3,4,5],[1,1,1]]
for i in range(len(p1s)):
    print(p1s[i],p2s[i],"dis=", cell_average.point_dis(np.array(p1s[i]),np.array(p2s[i])))
print("")



"""def dis_point_to_line(p1, p2, p3):
    Find distance from p1 to line p2p3
    return np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / point_dis(p2, p3)
"""
def tst_helen_s(p1,p2,p3):
    a = cell_average.point_dis(p1, p2)
    b = cell_average.point_dis(p2, p3)
    c = cell_average.point_dis(p1, p3)
    p = (a+b+c)/2
    s = p*(p-a)*(p-b)*(p-c)
    s = math.sqrt(s)
    return s
print("########test dis_point_to_line")
ps = [[1.1,2.3,4.5], [-0.5,0.9,10.0], [2.9,-1.0,2.1]]
p1 = np.array(ps[0])
p2 = np.array(ps[1])
p3 = np.array(ps[2])
s = tst_helen_s(p1,p2,p3)
print("points=",ps)
print("(need eq) ", cell_average.dis_point_to_line(p1,p2,p3), s*2.0/cell_average.point_dis(p2,p3))
print("(need eq) ", cell_average.dis_point_to_line(p2,p1,p3), s*2.0/cell_average.point_dis(p1,p3))
print("(need eq) ", cell_average.dis_point_to_line(p3,p2,p1), s*2.0/cell_average.point_dis(p2,p1))
print("")



"""def plane_intersection(p1, p2, plane):
    Find intersection of plane and line
    d1 = dis_point_to_plane(p1, plane)
    d2 = dis_point_to_plane(p2, plane)
    return p1 + (p2 - p1) * d1 / max(1e-9, (d1 - d2))
"""
def tst_check_3_points_in_line(p1,p2,p3):
    v1 = p3 - p1   
    v2 = p3 - p2
    print("is_parallel?(need eq) ",v1[0]/v2[0], v1[1]/v2[1], v1[2]/v2[2])    #need equal

print("########test plane_intersection")
p1 = np.array([1.0,2.3,4.5])
p2 = np.array([5.0,-2.0,6.1])
plane = [2.1, 1.5, -3.2, 4.7]
print(p1,p2,plane)
inter_p = cell_average.plane_intersection(p1, p2, plane)
print("inter point = ", inter_p)
tst_check_3_points_in_line(p1,p2,inter_p)
print("in_plane? (need=0)", tst_plane_res(plane, inter_p))              #need = 0
print("")



"""def line_intersection(p1, p2, p3, p4):
    Find intersection of line p1p2 and line p3p4
    d1 = dis_point_to_line(p1, p3, p4)
    d2 = dis_point_to_line(p2, p3, p4)
    return p1 + (p2 - p1) * d1 / max(1e-9, (d1 - d2))
"""
print("########test plane_intersection")
p1 = np.array([1.0,2.0,3.0])
p2 = np.array([-5.0,2.1,3.9])
p3 = np.array([-2.1,-9.0,1.5])
plane = cell_average.plane_from_3_points(p1,p2,p3)
print("plane = ", plane)
p4_x,p4_y = 3.1,4.1
p4_z = -(plane[0]*p4_x + plane[1]*p4_y + plane[3])/plane[2]
p4 = np.array([p4_x,p4_y,p4_z])
line_inter = cell_average.line_intersection(p1, p2, p3, p4)
tst_check_3_points_in_line(p1,p2,line_inter)
tst_check_3_points_in_line(p3,p4,line_inter)
print("")



"""def check_closure(point, p1, p2, p3, p4):
    Check whether point is in tetrahedron
    p1, p2, p3, p4 = np.array(p1), np.array(p2), np.array(p3), np.array(p4)
    f1 = plane_from_3_points(p2, p3, p4)
    f2 = plane_from_3_points(p1, p3, p4)
    f3 = plane_from_3_points(p1, p2, p4)
    f4 = plane_from_3_points(p1, p2, p3)
    return check_dis(point, p1, f1) and check_dis(point, p2, f2) and \
           check_dis(point, p3, f3) and check_dis(point, p4, f4)
"""
print("########test check_closure")
p1 = np.array([0.,0.,0.])
p2 = np.array([0.,0.,1.])
p3 = np.array([0.,1.,0.])
p4 = np.array([1.,0.,0.])
ps = [p1,p2,p3,p4,(p1+p2+p3+p4)/4, [-1.,-1.,-1], [0.5,0.5,0.5], [0.1,0.2,0.3], [1.,1.,1.]]
plane = cell_average.plane_from_3_points(p2, p3, p4)
print(p1,"dis=", cell_average.dis_point_to_plane(p1,plane)) 
for p in ps:
    print(p,"in tetrahedron?", cell_average.check_closure(p, p1, p2, p3, p4), "dis=", cell_average.dis_point_to_plane(p,plane))
print("")
