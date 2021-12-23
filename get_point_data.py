import numpy as np
import os.path
from data_preprocessing import data_preprocess
import cell_average
path = os.getcwd()


class GetPointData:
    def __init__(self, file_name, yz_pos, elem_size):
        """Initialize class"""
        self.grid_data = data_preprocess(file_name)
        self.file_name = file_name
        self.yz_node = []
        self.y_pos = yz_pos[0]
        self.z_pos = yz_pos[1]
        self.elem_size = elem_size
        self.max_x = 0

        self.node_tolerance = 1 * self.elem_size
        self.s_step = 1e-6 * self.elem_size
        self.solidification = 0.1
        self.load_data()
        self.find_domain_bound_x()

    def load_data(self):
        """Record and sort active node index and x position"""
        for point in self.grid_data.keys():
            if np.abs(self.grid_data[point][0]['y_pos'] - self.y_pos) <= self.elem_size + self.node_tolerance:
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

    def get_grid_point(self, index):  # index is src data file line index
        """Get point position with point index"""
        x = self.grid_data[index][0]['x_pos']
        y = self.grid_data[index][0]['y_pos']
        z = self.grid_data[index][0]['z_pos']
        return np.array([x, y, z])

    def get_tet_node(self, x_pos, y_pos, z_pos, active_node):
        """Get node of tetrahedron cell"""
        dst_p = np.array([x_pos, y_pos, z_pos])
        # active_node is src data file line index

        distance = []
        for index in active_node:
            tmp_point = np.array([self.grid_data[index][0]['x_pos'],
                                  self.grid_data[index][0]['y_pos'],
                                  self.grid_data[index][0]['z_pos']])
            distance.append(cell_average.point_dis(dst_p, tmp_point))

        top_index = sorted(range(len(distance)), key=lambda i: distance[i], reverse=False)

        treat_pnum = min(16, len(active_node))

        # print('---Nearest node index and distance:')
        # for i in range(treat_pnum):
        #     print(active_node[top_index[i]], distance[top_index[i]])

        tetrs = []
        for lp1 in range(0, treat_pnum):
            p1 = self.get_grid_point(active_node[top_index[lp1]])
            for lp2 in range(lp1 + 1, treat_pnum):
                p2 = self.get_grid_point(active_node[top_index[lp2]])
                for lp3 in range(lp2 + 1, treat_pnum):
                    p3 = self.get_grid_point(active_node[top_index[lp3]])
                    for lp4 in range(lp3 + 1, treat_pnum):
                        p4 = self.get_grid_point(active_node[top_index[lp4]])
                        if cell_average.check_closure(dst_p, p1, p2, p3, p4):
                            # print(p1,p2,p3,p4)
                            s = cell_average.tetrahedron_l(p1, p2, p3, p4)
                            tetrs.append([s, p1, p2, p3, p4,
                                          active_node[top_index[lp1]],
                                          active_node[top_index[lp2]],
                                          active_node[top_index[lp3]],
                                          active_node[top_index[lp4]]])
        # print('---Number of closed tetra:', len(tetrs))

        if len(tetrs) == 0:
            print('No legal tetrahedron found (get_point_data: get_tet_node). Location:', (x_pos, y_pos, z_pos), self.file_name)
            return [
                self.get_grid_point(active_node[top_index[0]]),
                self.get_grid_point(active_node[top_index[1]]),
                self.get_grid_point(active_node[top_index[2]]),
                self.get_grid_point(active_node[top_index[3]]),
                active_node[top_index[0]],
                active_node[top_index[1]],
                active_node[top_index[2]],
                active_node[top_index[3]]
            ]
        min_ind = sorted(range(len(tetrs)), key=lambda i: tetrs[i][0], reverse=False)[0]
        min_tetr = tetrs[min_ind][1:]
        # min_l = tetrs[min_ind][0]

        # print('---Tetra candidates (l less than 1.5*l_min)')
        # print("min:", min_tetr, min_l)
        # for nn in tetrs:
        #     if nn[0] < 1.5 * min_l:
        #         dp1 = ((nn[1][0] - x_pos) * 1000, (nn[1][1] - y_pos) * 1000, (nn[1][2] - z_pos) * 1000)
        #         dp2 = ((nn[2][0] - x_pos) * 1000, (nn[2][1] - y_pos) * 1000, (nn[2][2] - z_pos) * 1000)
        #         dp3 = ((nn[3][0] - x_pos) * 1000, (nn[3][1] - y_pos) * 1000, (nn[3][2] - z_pos) * 1000)
        #         dp4 = ((nn[4][0] - x_pos) * 1000, (nn[4][1] - y_pos) * 1000, (nn[4][2] - z_pos) * 1000)
        #         print('\nP1: ' + "%.4f,%.4f,%.4f" % dp1)
        #         print('P2: ' + "%.4f,%.4f,%.4f" % dp2)
        #         print('P3: ' + "%.4f,%.4f,%.4f" % dp3)
        #         print('P4: ' + "%.4f,%.4f,%.4f" % dp4)
        #         print('Index:', nn[5:], 'Length:', nn[0])

        # p1 = self.get_grid_point(active_node[top_index[0]])
        # p2 = self.get_grid_point(active_node[top_index[1]])
        # p3 = self.get_grid_point(active_node[top_index[2]])
        # p4 = self.get_grid_point(active_node[top_index[3]])
        # i1 = active_node[top_index[0]]
        # i2 = active_node[top_index[1]]
        # i3 = active_node[top_index[2]]
        # i4 = active_node[top_index[3]]
        # min_tetr = [p1, p2, p3, p4, i1, i2, i3, i4]

        # print('--------', min_tetr[-4:], end='')
        return min_tetr

    def node_tet_avg(self, x, y, z, tetra_node, data_type, check=False):
        """Get tetrahedron average on point"""
        dst_p = [x, y, z]
        [p1, p2, p3, p4, ind1, ind2, ind3, ind4] = tetra_node

        nodes = [p1, p2, p3, p4]
        values = []
        for ind in [ind1, ind2, ind3, ind4]:
            values.append(self.grid_data[ind][0][data_type])

        return cell_average.tetrahedron_average(dst_p, nodes, values, check=check)

    def gradient(self, x_pos, tetra_node, data_type):
        """Compute gradient"""
        x_high = self.node_tet_avg(x_pos + self.s_step, self.y_pos, self.z_pos, tetra_node, data_type, check=False)
        x_low = self.node_tet_avg(x_pos - self.s_step, self.y_pos, self.z_pos, tetra_node, data_type, check=False)
        x_gradient = (x_high - x_low) / (2 * self.s_step)

        y_high = self.node_tet_avg(x_pos, self.y_pos + self.s_step, self.z_pos, tetra_node, data_type, check=False)
        y_low = self.node_tet_avg(x_pos, self.y_pos - self.s_step, self.z_pos, tetra_node, data_type, check=False)
        y_gradient = (y_high - y_low) / (2 * self.s_step)

        z_high = self.node_tet_avg(x_pos, self.y_pos, self.z_pos + self.s_step, tetra_node, data_type, check=False)
        z_low = self.node_tet_avg(x_pos, self.y_pos, self.z_pos - self.s_step, tetra_node, data_type, check=False)
        z_gradient = (z_high - z_low) / (2 * self.s_step)

        return x_gradient, y_gradient, z_gradient

    def get_neighbor_cent(self, x_pos, active_node, closest_neighbor=False):
        """Find cell containing the point and all neighboring cells"""
        distance = []
        dst_p = np.array([x_pos, self.y_pos, self.z_pos])
        for index in active_node:
            tmp_point = np.array([self.grid_data[index][0]['x_pos'],
                                  self.grid_data[index][0]['y_pos'],
                                  self.grid_data[index][0]['z_pos']])
            distance.append(cell_average.point_dis(dst_p, tmp_point))
        min_distance = min(distance)
        cell_cent = active_node[distance.index(min_distance)]

        if closest_neighbor:
            distance = []
            dst_p = np.array([self.grid_data[cell_cent][0]['x_pos'],
                              self.grid_data[cell_cent][0]['y_pos'],
                              self.grid_data[cell_cent][0]['z_pos']])
            for index in active_node:
                tmp_point = np.array([self.grid_data[index][0]['x_pos'],
                                      self.grid_data[index][0]['y_pos'],
                                      self.grid_data[index][0]['z_pos']])
                distance.append(cell_average.point_dis(dst_p, tmp_point))
            top_index = sorted(range(len(distance)), key=lambda i: distance[i], reverse=False)
            surr_cent = []
            for ind in top_index[1:1+4]:
                surr_cent.append(active_node[ind])
        else:
            surr_cent = []
            dst_p = np.array([self.grid_data[cell_cent][0]['x_pos'],
                              self.grid_data[cell_cent][0]['y_pos'],
                              self.grid_data[cell_cent][0]['z_pos']])
            for index in active_node:
                tmp_point = np.array([self.grid_data[index][0]['x_pos'],
                                      self.grid_data[index][0]['y_pos'],
                                      self.grid_data[index][0]['z_pos']])
                if cell_average.point_dis(dst_p, tmp_point) <= self.elem_size * 2:
                    surr_cent.append(index)
            # print(len(surr_cent))

        # cent_p = ((self.grid_data[cell_cent][0]['x_pos'] * 1000,
        #        self.grid_data[cell_cent][0]['y_pos'] * 1000,
        #        self.grid_data[cell_cent][0]['z_pos'] * 1000))
        # print(f'Centroid P: ' + "%.4f,%.4f,%.4f" % cent_p)
        # for i in range(4):
        #     dp = ((self.grid_data[surr_cent[i]][0]['x_pos'] * 1000,
        #            self.grid_data[surr_cent[i]][0]['y_pos'] * 1000,
        #            self.grid_data[surr_cent[i]][0]['z_pos'] * 1000))
        #     print(f'Neighbor P{i+1}: ' + "%.4f,%.4f,%.4f" % dp)
        # for i in range(4):
        #     dp = (self.grid_data[surr_cent[i]][0]['x_pos'] * 1000 - cent_p[0],
        #           self.grid_data[surr_cent[i]][0]['y_pos'] * 1000 - cent_p[1],
        #           self.grid_data[surr_cent[i]][0]['z_pos'] * 1000 - cent_p[2])
        #     print(f'Displacement P{i+1}: ' + "%.4f,%.4f,%.4f" % dp)

        return cell_cent, surr_cent

    def least_square_gradient(self, cell_cent, surr_cent,data_type='temperature'):
        """Compute gradient at cell centroid using least squares method"""
        geo_matrix = []
        diff_matrix = []

        cent_x = self.grid_data[cell_cent][0]['x_pos']
        cent_y = self.grid_data[cell_cent][0]['y_pos']
        cent_z = self.grid_data[cell_cent][0]['z_pos']
        cent_val = self.grid_data[cell_cent][0][data_type]

        for neighbor in surr_cent:
            geo_matrix.append([
                self.grid_data[neighbor][0]['x_pos'] - cent_x,
                self.grid_data[neighbor][0]['y_pos'] - cent_y,
                self.grid_data[neighbor][0]['z_pos'] - cent_z
            ])
            diff_matrix.append(self.grid_data[neighbor][0][data_type] - cent_val)

        cent_grad = np.linalg.lstsq(geo_matrix, diff_matrix, rcond=None)[0]
        return cent_grad[0], cent_grad[1], cent_grad[2]

    def get_active_node(self, x_pos):
        anchor_node = self.node_binary_search(x_pos)
        active_node = []
        i = 0
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
            if anchor_node - j == 0:
                break
            node_index = self.yz_node[anchor_node - j][0]
            if np.abs(self.grid_data[node_index][0]['x_pos'] - x_pos) > self.elem_size + self.node_tolerance:
                break
            else:
                active_node.append(node_index)
            j += 1
        return active_node

    def get_point_data(self, x_pos, info=False, lf=False):
        """Get data of specific point by spacial linear average of element nodes"""
        # find approximate range of x_pos in nodes
        active_node = self.get_active_node(x_pos)
        tetra_node = self.get_tet_node(x_pos, self.y_pos, self.z_pos, active_node)
        # Liquid_fraction
        if lf:
            liquid_fraction = self.node_tet_avg(x_pos, self.y_pos, self.z_pos, tetra_node, 'liquid_fraction')
        temperature = self.node_tet_avg(x_pos, self.y_pos, self.z_pos, tetra_node, 'temperature')

        # x = self.node_tet_avg(x_pos, self.y_pos, self.z_pos, tetra_node, 'x_pos')
        # y = self.node_tet_avg(x_pos, self.y_pos, self.z_pos, tetra_node, 'y_pos')
        # z = self.node_tet_avg(x_pos, self.y_pos, self.z_pos, tetra_node, 'z_pos')
        # return y - self.y_pos, self.gradient(x_pos, tetra_node, 'y_pos')

        if lf:
            if not info:
                # not ice front
                return liquid_fraction, temperature
            else:
                # get temperature and temperature gradient
                return [liquid_fraction, self.gradient(x_pos, tetra_node, 'liquid_fraction')], \
                       [temperature, self.gradient(x_pos, tetra_node, 'temperature')]
        else:
            if not info:
                # not ice front
                return None, temperature
            else:
                # get temperature and temperature gradient
                cell_cent, surr_cent = self.get_neighbor_cent(x_pos, active_node)
                temp_gradient = self.least_square_gradient(cell_cent, surr_cent)
                return None, [temperature, temp_gradient]

    def find_domain_bound_x(self):
        for i in range(len(self.yz_node)-1):
            if self.yz_node[i+1][1] - self.yz_node[i][1] > 5 * self.elem_size:
                self.max_x = self.yz_node[i][1]
                break

