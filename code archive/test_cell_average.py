import cell_average as ca
import numpy as np

# print('\n-----Tetra Closure Test-----')
# p = [0.005, 0.002, -0.005]
# p1 = [0.00495982,  0.00201709, -0.00514187]
# p2 = [0.00503642,  0.00189178, -0.00486913]
# p3 = [0.0047878,  0.00179231, -0.00486921]
# p4 = [0.00471121,  0.00191762, -0.00514194]
#
# p1, p2, p3, p4 = np.array(p1), np.array(p2), np.array(p3), np.array(p4)
# f1 = ca.plane_from_3_points(p2, p3, p4)
# f2 = ca.plane_from_3_points(p1, p3, p4)
# f3 = ca.plane_from_3_points(p1, p2, p4)
# f4 = ca.plane_from_3_points(p1, p2, p3)
#
# print('Node 1:', ca.check_dis(p, p1, f1))
# print('Node 2:', ca.check_dis(p, p2, f2))
# print('Node 3:', ca.check_dis(p, p3, f3))
# print('Node 4:', ca.check_dis(p, p4, f4))
#
# print('Closure:', ca.check_closure(p, p1, p2, p3, p4))
# print('-----Tetra Closure Test END-----')


print('\n-----Tetra Average Test-----')
point = [2/3, 0, 0]
nodes = [[0, 0, 2], [1, -np.sqrt(1/3), 0], [-1, -np.sqrt(1/3), 0], [0, 2*np.sqrt(1/3), 0]]
value = []
for node in nodes:
    value.append(node[0])
print('Point:', point)
print('Node value:', value)
print('calculated point value:', ca.tetrahedron_average(point, nodes, value))
print('-----Tetra Average Test END-----')

