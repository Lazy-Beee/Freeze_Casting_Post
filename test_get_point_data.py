import data_preprocessing as dp
import get_point_data as gpd


file_name = ['center-0300', 'node-0300']
element_size = 5e-4
x = 0.005
y = 0.002
z = -0.005

# node_data = dp.data_preprocess(file_name)
# print('\n-----Data Processing Test-----')
# print(f'Data length: {len(node_data)}')
# print(node_data[1])
# print(node_data[len(node_data)])
# print('-----Data Processing Test-----')

a = gpd.GetPointData(file_name, [y, z], element_size)
# print('\n-----Tetrahedron search Test-----')
# active_node = a.get_active_node(x)
# print('---Number of node within search range:', len(active_node), '. Node index:')
# print(active_node)
# a.get_tet_node(x, y, z, active_node)

n = 10
for i in range(n):
    start = 0.00685
    end = 0.0069
    x_pos = start + i * (end - start) / (n - 1)
    print('%.6f' % x_pos, a.get_ice_front_data(x_pos))
# print(a.get_ice_front_data(0.0069, info=True))

print('-----Tetrahedron search Test-----')
