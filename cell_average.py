import numpy as np


def plane_from_3_points(p1, p2, p3):
    """Find plane equation ax+by+cd+d=0, return [a,b,c,d]"""
    a = (p2[1] - p1[1]) * (p3[2] - p1[2]) - (p3[1] - p1[1]) * (p2[2] - p1[2])
    b = (p2[2] - p1[2]) * (p3[0] - p1[0]) - (p3[2] - p1[2]) * (p2[0] - p1[0])
    c = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    d = - (a * p1[0] + b * p1[1] + c * p1[2])
    return [a, b, c, d]


def dis_point_to_plane(point, plane):
    """Find distance (directional) form point to plane"""
    [x, y, z] = point
    [a, b, c, d] = plane
    if abs(a*x + b*y + c*z + d) == 0:
        return 0
    return (a*x+b*y+c*z+d)/np.linalg.norm([a, b, c])


def point_dis(p1, p2):
    """Distance between two points"""
    return np.linalg.norm(p1 - p2)


def dis_point_to_line(p1, p2, p3):
    """Find distance from p1 to line p2p3"""
    return np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / point_dis(p2, p3)


def plane_intersection(p1, p2, plane):
    """Find intersection of plane and line"""
    d1 = dis_point_to_plane(p1, plane)
    d2 = dis_point_to_plane(p2, plane)

    # print('\n---Plane Intersection')
    # print('Point 1:', p1)
    # print('Point 2:', p2)
    # print('Plane:', plane)
    # print('Distance 1:', d1)
    # print('Distance 2:', d2)
    # print('Intersection on face:', p1 + (p2 - p1) * d1 / (d1 - d2))
    # print('---Plane Intersection END')

    if d1 == d2:
        print('Parallel line in finding plane intersection')
    elif d2 == 0:
        return p2
    elif d1 == 0:
        return p1
    else:
        return p1 + (p2 - p1) * d1 / (d1 - d2)


def line_intersection(p1, p2, p3, p4):
    """Find intersection of line p1p2 and line p3p4"""
    d1 = dis_point_to_line(p1, p3, p4)
    d2 = dis_point_to_line(p2, p3, p4)
    if d1 == d2:
        print('Parallel line in finding line intersection')
    elif d2 == 0:
        return p2
    elif d1 == 0:
        return p1
    else:
        return p1 + (p2 - p1) * d1 / (d1 - d2)


def check_dis(point, node, plane):
    """Check if the point is further away from the plane than the node"""
    dis_point = dis_point_to_plane(point, plane)
    dis_node = dis_point_to_plane(node, plane)
    # print(dis_node, dis_point)
    if np.sign(dis_node) == np.sign(dis_point) and abs(dis_node) >= abs(dis_point):
        return True
    elif dis_point == 0:
        return True
    else:
        return False


def check_closure(point, p1, p2, p3, p4):
    """Check whether point is in tetrahedron"""
    p1, p2, p3, p4 = np.array(p1), np.array(p2), np.array(p3), np.array(p4)
    f1 = plane_from_3_points(p2, p3, p4)
    f2 = plane_from_3_points(p1, p3, p4)
    f3 = plane_from_3_points(p1, p2, p4)
    f4 = plane_from_3_points(p1, p2, p3)
    return check_dis(point, p1, f1) and check_dis(point, p2, f2) and \
           check_dis(point, p3, f3) and check_dis(point, p4, f4)


def tetrahedron_average(point, nodes, values, check=True):
    """Find point value from nodes of tetrahedron"""
    point = np.array(point)
    [p1, p2, p3, p4] = nodes
    p1, p2, p3, p4 = np.array(p1), np.array(p2), np.array(p3), np.array(p4)
    f1 = plane_from_3_points(p2, p3, p4)
    # Check is point is on the node
    if np.linalg.norm(point - p1) < 1e-9:
        return values[0]
    elif np.linalg.norm(point - p2) < 1e-9:
        return values[1]
    elif np.linalg.norm(point - p3) < 1e-9:
        return values[2]
    elif np.linalg.norm(point - p4) < 1e-9:
        return values[3]

    # Check whether point is in tetrahedron
    elif (not check) or check_closure(point, p1, p2, p3, p4):
        # Find face point on plane p2p3p4
        p_face = plane_intersection(p1, point, f1)
        # Find edge point on line p3p4
        p_edge = line_intersection(p2, p_face, p3, p4)

        # Find value of edge point
        weight_edge = [1 / max(1e-9, point_dis(p_edge, p3)), 1 / max(1e-9, point_dis(p_edge, p4))]
        value_edge = np.average([values[2], values[3]], weights=weight_edge)
        # Find value of face point
        weight_face = [1 / max(1e-9, point_dis(p_edge, p_face)), 1 / max(1e-9, point_dis(p_face, p2))]
        value_face = np.average([value_edge, values[1]], weights=weight_face)
        # Find value of body point
        weight_body = [1 / max(1e-9, point_dis(point, p_face)), 1 / max(1e-9, point_dis(point, p1))]
        value_body = np.average([value_face, values[0]], weights=weight_body)

        # print('\n---Tetra Average')
        # print('Body point:', np.ndarray.tolist(point))
        # print('Face point:', np.ndarray.tolist(p_face))
        # print('Edge point:', np.ndarray.tolist(p_edge))
        # print('Edge weight', weight_edge, '    Edge value', value_edge)
        # print('Face weight', weight_face, '    Face value', value_face)
        # print('Body weight', weight_body, '    Body value', value_body)
        # print('---Tetra Average END')

        return value_body

    else:
        return None


def tetrahedron_v(p1, p2, p3, p4):
    """Find volume of tetrahedron"""
    plane = plane_from_3_points(p1, p2, p3)
    dis = abs(dis_point_to_plane(p4, plane))
    triangle_s = np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / 2.0
    return dis * triangle_s / 6.0


def tetrahedron_s(p1, p2, p3, p4):
    """Find volume of tetrahedron"""
    triangle_s = np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / 2.0
    triangle_s += np.linalg.norm(np.cross(p2 - p1, p4 - p1)) / 2.0
    triangle_s += np.linalg.norm(np.cross(p3 - p1, p4 - p1)) / 2.0
    triangle_s += np.linalg.norm(np.cross(p2 - p3, p4 - p3)) / 2.0
    return triangle_s


def tetrahedron_l(p1, p2, p3, p4):
    """Find volume of tetrahedron"""
    points = [p1, p2, p3, p4]
    l_sum = 0
    for p1 in points:
        for p2 in points:
            l_sum += point_dis(p1, p2)
    return l_sum


# def cuboid_xy_face_average(cube_xyz, point_xyz, values):
#     """Value of point on rectangular face, node are ordered in CW direction"""
#     weight_x = [1 / max(1e-9, point_xyz[0]), 1 / max(1e-9, cube_xyz[0] - point_xyz[0])]
#     weight_y = [1 / max(1e-9, point_xyz[1]), 1 / max(1e-9, cube_xyz[1] - point_xyz[1])]
#     value_y = [np.average([values[0], values[1]], weights=weight_x),
#                np.average([values[3], values[2]], weights=weight_x)]
#     return np.average(value_y, weights=weight_y)


# def cuboid_average(point, nodes, values):
#     """Point value in cuboid element"""
#     point = np.array(point)
#     nodes = np.array(nodes)
#     x_max = np.max([node[0] for node in nodes])
#     x_min = np.min([node[0] for node in nodes])
#     y_max = np.max([node[1] for node in nodes])
#     y_min = np.min([node[1] for node in nodes])
#     z_max = np.max([node[2] for node in nodes])
#     z_min = np.min([node[2] for node in nodes])
#     cube_xyz = [x_max - x_min, y_max - y_min, z_max - z_min]
#     point_xyz = [point[0] - x_min, point[1] - y_min, point[2] - z_min]
#
#     # Check if point is in element
#     for x in point_xyz:
#         if x < 0:
#             print('Error in point position (cuboid)')
#             return False, None
#
#     # Order nodes and values
#     ordered_nodes = np.array([[x_min, y_min, z_min], [x_max, y_min, z_min],
#                               [x_max, y_max, z_min], [x_min, y_max, z_min],
#                               [x_min, y_min, z_max], [x_max, y_min, z_max],
#                               [x_max, y_max, z_max], [x_min, y_max, z_max]])
#     ordered_values = [-1] * 8
#     for i, node in enumerate(nodes):
#         for j, ordered_node in enumerate(ordered_nodes):
#             if np.linalg.norm(node-ordered_node) < 1e-3:
#                 ordered_values[j] = values[i]
#     if -1 in ordered_values:
#         print('Error in cuboid node assignment')
#         return False, None
#
#     # Find point value
#     weight_z = [1 / max(1e-9, point_xyz[2]), 1 / max(1e-9, cube_xyz[2] - point_xyz[2])]
#     value_z = [cuboid_xy_face_average(cube_xyz, point_xyz, ordered_values[:4]),
#                cuboid_xy_face_average(cube_xyz, point_xyz, ordered_values[4:])]
#     return True, np.average(value_z, weights=weight_z)
