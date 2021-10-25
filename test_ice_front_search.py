import ice_front_search as ifs
from tqdm import trange

# print('\n-----finger location test-----')
# for i in range(9):
#     yz = [0, -9e-3/9 * i]
#     print(yz, ifs.finger_location(yz))
# for i in range(10):
#     yz = [-5e-3 + 10e-3/10*(i+1), 0]
#     print(yz, ifs.finger_location(yz))
# print('-----finger location test END-----')

print('\n-----YZ search test-----')
# for i in range(7):
#     yz = [0, -1e-3 * (i + 1)]
#     print(yz, ifs.yz_search_temp(yz)[1])

# for i in range(9):
#     yz = [-1e-3 * (i - 4), -4.5e-3]
#     print(yz, ifs.yz_search_temp(yz))

for i in range(7):
    yz = [0, -1e-3 * (i + 1)]
    a = ifs.yz_search(yz)
    print('---', yz, a[0])
    print(a[1][0])
    print(a[1][1])

for i in range(9):
    yz = [-1e-3 * (i - 4), -4.5e-3]
    a = ifs.yz_search(yz)
    print('---', yz, a[0])
    print(a[1][0])
    print(a[1][1])

print('-----YZ search test END-----')
