import sys

input_n = int(sys.stdin.readline().strip().split()[0])
lights_list = list(map(int, sys.stdin.readline().strip().split()))

left_off_count = 0
for light in lights_list:
    if light != 0:
        break
    else:
        left_off_count = left_off_count + 1

on_count = 0
off_count = 0
for light in lights_list[left_off_count:]:
    if light != 0:
        on_count = on_count + 1
    else:
        off_count = off_count + 1

if ((on_count - off_count) % 2 == 0):
    print('Alice')
else:
    print('Bob')