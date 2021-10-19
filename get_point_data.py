import numpy as np
import matplotlib.pyplot as plt
import os.path
from data_preprocessing import data_preprocess
import cell_average
path = os.getcwd()


class GetPointData:
    def __init__(self, file_name, yz_pos, elem_size, moving_zone_range):
        """Initialize class"""
        # with open(os.path.dirname(path) + f'\processed_data\{file_name}.csv') as f:
        #     content = csv.reader(f)
        #     self.grid_data = {rows[0]: rows[1] for rows in content}
        #     f.close()

        self.grid_data = data_preprocess(file_name)
        self.file_name = file_name
        self.yz_node = []
        self.y_pos = yz_pos[0]
        self.z_pos = yz_pos[1]
        self.elem_size = elem_size
        self.moving_lower_bound = moving_zone_range[0]
        self.moving_upper_bound = moving_zone_range[1]

        self.node_tolerance = 1 * self.elem_size
        self.small_distance = 1e-6 * self.elem_size
        self.solidification = 0.1
        self.load_data()

    def load_data(self):
        """Record and sort active node index and x position"""
        for point in self.grid_data.keys():
            # print(np.abs(self.grid_data[point][0]['y_pos'] - self.y_pos))
            if np.abs(self.grid_data[point][0]['y_pos'] - self.y_pos) <= self.elem_size + self.node_tolerance:
                # print(np.abs(self.grid_data[point][0]['z_pos'] - self.z_pos))
                if np.abs(self.grid_data[point][0]['z_pos'] - self.z_pos) <= self.elem_size + self.node_tolerance:
                    self.yz_node.append((point, self.grid_data[point][0]['x_pos']))
        self.yz_node.sort(key=lambda x: x[1])

    def node_binary_search(self, x_pos):
        """Search for x position in range"""
        low, high = 0, len(self.yz_node)
        while True:
            if high >= low:
                mid = (low + high) // 2
                # print(low, high, mid)
                if abs(self.yz_node[mid][1] - x_pos) <= self.elem_size + self.node_tolerance:
                    return mid
                elif self.yz_node[mid][1] - x_pos > self.elem_size + self.node_tolerance:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                print('Binary search failed (1)')
                return -1

    def node_data_avg(self, x_pos, y_pos, z_pos, active_node, data_type, node_num):
        """Get spatial node data average"""
        point = np.array([x_pos, y_pos, z_pos])
        value, node_pos, distance = [], [], []
        for node_index in active_node:
            value.append(self.grid_data[node_index][0][data_type])
            node_pos.append(np.array([self.grid_data[node_index][0]['x_pos'],
                                      self.grid_data[node_index][0]['y_pos'],
                                      self.grid_data[node_index][0]['z_pos']]))
            distance.append(np.linalg.norm(node_pos[-1] - point))
        top_index = sorted(range(len(distance)), key=lambda i: distance[i], reverse=True)   # TODO: check order
        if node_num == 8:
            top_value = [value[i] for i in top_index[:node_num]]
            top_node = [node_pos[i] for i in top_index[:node_num]]
            # print(node_num, top_node, top_value)
            return cell_average.tetrahedron_average(point, top_node, top_value)[1]
        else:
            top_value = [value[i] for i in top_index[:3]]
            top_node = [node_pos[i] for i in top_index[:3]]
            face = cell_average.plane_from_3_points(top_node[0], top_node[1], top_node[2])
            for i in top_index[3:]:
                if cell_average.check_dis(point, node_pos[top_index[i]], face):   # TODO: check closure
                    top_node.append(node_pos[top_index[i]])
                    top_value.append(value[top_index[i]])
                    break
            # print(node_num, top_node, top_value)
            return cell_average.tetrahedron_average(point, top_node, top_value)[1]

    def gradient(self, x_pos, active_node, data_type, node_num):
        x_high = self.node_data_avg(x_pos + self.small_distance, self.y_pos, self.z_pos, active_node, data_type, node_num)
        x_low = self.node_data_avg(x_pos - self.small_distance, self.y_pos, self.z_pos, active_node, data_type, node_num)
        x_gradient = (x_high - x_low) / (2 * self.small_distance)

        y_high = self.node_data_avg(x_pos, self.y_pos + self.small_distance, self.z_pos, active_node, data_type, node_num)
        y_low = self.node_data_avg(x_pos, self.y_pos - self.small_distance, self.z_pos, active_node, data_type, node_num)
        y_gradient = (y_high - y_low) / (2 * self.small_distance)

        z_high = self.node_data_avg(x_pos, self.y_pos, self.z_pos + self.small_distance, active_node, data_type, node_num)
        z_low = self.node_data_avg(x_pos, self.y_pos, self.z_pos - self.small_distance, active_node, data_type, node_num)
        z_gradient = (z_high - z_low) / (2 * self.small_distance)

        return x_gradient, y_gradient, z_gradient

    def get_ice_front_data(self, x_pos, info=False):
        """Get data of specific point by spacial linear average of element nodes"""
        # find approximate range of x_pos in nodes
        anchor_node = self.node_binary_search(x_pos)
        active_node = [anchor_node]
        i = 1
        while True:
            if anchor_node + i >= len(self.yz_node):
                break
            node_index = self.yz_node[anchor_node + i][0]
            if np.abs(self.grid_data[node_index][0]['x_pos'] - x_pos) > self.elem_size + self.node_tolerance:
                break
            else:
                active_node.append(node_index)
            i += 1
        j = 1
        while True:
            if anchor_node - j < 0:
                break
            node_index = self.yz_node[anchor_node - j][0]
            if np.abs(self.grid_data[node_index][0]['x_pos'] - x_pos) > self.elem_size + self.node_tolerance:
                break
            else:
                active_node.append(node_index)
            j += 1

        # determine element type
        # active_node_new = []
        # if self.moving_lower_bound < x_pos < self.moving_upper_bound:
        #     # find tetrahedron element nodes
        #     for node in active_node:
        #         if self.moving_lower_bound <= self.grid_data[node][0]['x_pos'] <= self.moving_upper_bound:
        #             active_node_new.append(node)
        #     node_num = 4
        # else:
        #     # cuboid nodes
        #     for node in active_node:
        #         if not self.moving_lower_bound < self.grid_data[node][0]['x_pos'] < self.moving_upper_bound:
        #             active_node_new.append(node)
        #     node_num = 8
        # active_node = active_node_new
        node_num = 4

        # Liquid_fraction
        if len(active_node) == 0:
            liquid_fraction = 10
        else:
            liquid_fraction = self.node_data_avg(x_pos, self.y_pos, self.z_pos, active_node, 'liquid_fraction', node_num)

        if not info:
            # not ice front
            return liquid_fraction, None
        else:
            # get temperature and temperature gradient
            temperature = self.node_data_avg(x_pos, self.y_pos, self.z_pos, active_node, 'temperature', node_num)
            return [liquid_fraction, self.gradient(x_pos, active_node, 'liquid_fraction', node_num)], \
                   [temperature, self.gradient(x_pos, active_node, 'temperature', node_num)]


if __name__ == '__main__':
    moving_zone = [1e-3 + 10 * 1e-6, 26e-3 + 10 * 1e-6]
    a = GetPointData('FFF-0200', [3.25e-3, -3.25e-3], 0.5e-3, moving_zone)
    for i in range(30, 120):
        print(a.get_ice_front_data(i*1e-4))

    # low, high = 0, 8e-3
    # while True:
    #     if high >= low:
    #         mid = (low + high) / 2
    #         print(mid)
    #         if 0 < a.get_ice_front_data(mid)[1] < 0.05:
    #             break
    #         elif 0.05 <= a.get_ice_front_data(mid)[0]:
    #             high = mid
    #         else:
    #             low = mid
    # print(a.get_ice_front_data(mid, info=True), mid)

