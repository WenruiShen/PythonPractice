import sys 
'''
for line in sys.stdin:
    a = line.split()
    print(int(a[0]) + int(a[1]))
'''

for line in sys.stdin:
    input_list = line.split()
    n_str = input_list[0]
    n_int = int(n_str)
    n_str_reverse = n_str[::-1]
    n_int_reverse = int(n_str_reverse)
    #print(n_int)
    #print(n_int_reverse)
    print(n_int + n_int_reverse)
    