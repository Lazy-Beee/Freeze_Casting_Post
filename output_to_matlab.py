import json
import os.path
path = os.getcwd()


def ice_front_to_table(in_file_name, out_file_name):
    with open(in_file_name, 'r') as in_file:
        data = json.load(in_file)
        in_file.close()

    with open(out_file_name, 'w') as out_file:
        for key in data:
            line = key
            for elem in data[key][2]:
                line += ' ' + str(elem)
            line += '\n'
            out_file.write(line)


in_file_name = os.path.dirname(path) + f'\\images\\11-11-2021\\90-5-162-30cp\\data.txt'
out_file_name = os.path.dirname(path) + f'\\images\\11-11-2021\\90-5-162-30cp\\data_table.txt'
ice_front_to_table(in_file_name, out_file_name)
