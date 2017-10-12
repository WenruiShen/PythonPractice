import sys
'''
360 test:
7 20
4 5 2 12 5 12 12 
4 20
10 10 10 10
4 12
5 5 5 5
'''

line_1_list = sys.stdin.readline().strip().split()
game_n = int(line_1_list[0])
max_t = int(line_1_list[1])
    
line_2 = sys.stdin.readline().strip()
item_time_list = list(map(int, line_2.split()))

sum_time = 0
max_sum_time = 0

# select the max item time;
max_item_time = 0
for item_time in item_time_list:
    if item_time > max_item_time:
        max_item_time = item_time

max_id = 0
item_len = len(item_time_list)
item_id = 0
for item_time in item_time_list:
    if item_time == max_item_time:
        max_id = item_id
        break
    item_id = item_id+1

item_time_list.pop(max_id)
#print(max_item_time)
#print(item_time_list)

# select from remaining items;
def select_one_item(item_time_list, sel_id, sum_time):
    global max_sum_time
    item_len = len(item_time_list)
    this_item_time = item_time_list[sel_id]
    sum_time_temp = sum_time + this_item_time
    if (sum_time_temp >= max_t) or (sel_id >= item_len - 1):
        if sum_time > max_sum_time:
            max_sum_time = sum_time
    elif sum_time_temp < max_t:
        while(sel_id < item_len):
            #max_sum_time = 
            select_one_item(item_time_list, sel_id, sum_time_temp)
            sel_id = sel_id + 1
    #return max_sum_time

item_id = 0
item_len = len(item_time_list)
while(item_id < item_len):
    #max_sum_time = 
    select_one_item(item_time_list, item_id, sum_time)
    item_id = item_id + 1
    
if max_sum_time < max_t:
    max_sum_time = max_sum_time + max_item_time
print(max_sum_time)