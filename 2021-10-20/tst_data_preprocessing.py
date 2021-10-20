import numpy as np
import data_preprocessing as dpp

import os.path
path = os.getcwd()

file_name = 'FFF-0100'
strs = ['x_pos', 'y_pos', 'z_pos', 'temperature', 'liquid_fraction']

#get file original info

# Read file
with open(os.path.dirname(path) + f'\data\{file_name}') as in_file:
    print("1st line:", in_file.readline())
    print("2nd line:", in_file.readline())
    print("3rd line:", in_file.readline())    
    content = in_file.readlines()
    print("last line:",content[-1])
    src_items_num = len(content)+2
    print("total data items num=", src_items_num)
    in_file.close()

node_data = dpp.data_preprocess(file_name)
print("node_data len=", len(node_data))
print("1:",node_data[1])
print("2:",node_data[2])
print(src_items_num,":",node_data[src_items_num])

for s in strs:
    lst = [value[0][s] for value in node_data.values()]
    print("len=",len(lst), s,"-- min=",min(lst),"max=",max(lst))
    



