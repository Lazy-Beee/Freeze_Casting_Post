import time
import numpy as np
import matplotlib.pyplot as plt
import os.path
path = os.getcwd()


def data_preprocess(file_names, write=False, plot=False, element_size=5e-4):
    time_start = time.time()
    node_data = {}
    ind_num = 0
    for file_name in file_names:
        # Read file
        with open(os.path.dirname(path) + f'\data\{file_name}') as in_file:
            in_file.readline()
            content = in_file.readlines()
            in_file.close()

        # Write into dictionary
        for line in content:
            line = line.split(' ')
            line.pop()
            while '' in line:
                line.remove('')

            for n, number in enumerate(line):
                if 'E' in number:
                    number.replace('E', 'e')
                line[n] = float(number)

            if line[4] != 0:
                node_data[int(line[0]) + ind_num] = []
                if len(line) == 6:
                    node_data[int(line[0]) + ind_num].append({
                        'x_pos': line[1], 'y_pos': line[2], 'z_pos': line[3],
                        'temperature': line[4], 'liquid_fraction': line[5]
                    })
                elif len(line) == 5:
                    node_data[int(line[0]) + ind_num].append({
                        'x_pos': line[1], 'y_pos': line[2], 'z_pos': line[3],
                        'temperature': line[4]
                    })
                else:
                    print('---WARNING--- Missing information in data (data_preprocess)')
        ind_num = len(node_data)
    # print(f'Data read from {file_names}, number of node read: {len(node_data)}')

    # Write to file
    if write:
        with open(os.path.dirname(path) + f'\processed_data\{file_name}.csv', 'w+') as out_file:
            for key in node_data.keys():
                out_file.write("%s,%s\n" % (key, node_data[key]))
            out_file.close()

    if plot:
        # Plot liquid fraction
        low = (0, 1, 0)
        medium = (0, 0, 1)
        high = (1, 0, 0)
        x_pos = []
        z_pos = []
        lf = []

        for node in node_data:
            if np.abs(node_data[node][0]['y_pos']) < element_size:
                x_pos.append(node_data[node][0]['x_pos'])
                z_pos.append(node_data[node][0]['z_pos'])
                if node_data[node][0]['liquid_fraction'] == 0.0:
                    lf.append(medium)
                elif node_data[node][0]['liquid_fraction'] == 1.0:
                    lf.append(high)
                else:
                    lf.append(low)

        plt.scatter(x=x_pos, y=z_pos, c=lf)
        plt.savefig(file_name + ' XZ-mid-LF')
        plt.close()

    return node_data
