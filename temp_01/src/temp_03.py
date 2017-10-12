# -*- coding:utf-8 -*-  
import sys
import copy

###############################################################################
# 魔法王国一共有n个城市,编号为0~n-1号,n个城市之间的道路连接起来恰好构成一棵树。
# 小易现在在0号城市,每次行动小易会从当前所在的城市走到与其相邻的一个城市,小易最多能行动L次。
# 如果小易到达过某个城市就视为小易游历过这个城市了,小易现在要制定好的旅游计划使他能游历最多的城市,
# 请你帮他计算一下他最多能游历过多少个城市(注意0号城市已经游历了,游历过的城市不重复计算)。 
# 输入描述:
# 输入包括两行,第一行包括两个正整数n(2 ≤ n ≤ 50)和L(1 ≤ L ≤ 100),表示城市个数和小易能行动的次数。
# 第二行包括n-1个整数parent[i](0 ≤ parent[i] ≤ i), 对于每个合法的i(0 ≤ i ≤ n - 2),在(i+1)号城市和parent[i]间有一条道路连接。
# 输出描述:输出一个整数,表示小易最多能游历的城市数量。
# 输入例子1:
# 5 2
# 0 1 2 3
# 输出例子1:3
# 3 2
# 0 0
# 测试用例:# 45 73
# 0 0 0 1 0 0 3 5 6 8 7 9 1 10 1 2 15 6 8 11 14 17 8 14 3 21 23 3 21 15 12 5 21 31 11 13 7 17 20 26 28 16 36 26
# 对应输出应该为:
41
###############################################################################

#max_visted_city = 0

def find_next_step(current_city_id, visited_city_list, parent_id_list, step_count):
    global max_visited_cities_num
    global city_n
    global step_L
    
    visited_city_list = copy.deepcopy(visited_city_list)
    
    # insert current city:
    if (current_city_id not in visited_city_list):
        visited_city_list.append(current_city_id)
    
    #print(str(current_city_id) + ', ' + str(visited_city_list) + ', ' + str(step_count))
    
    # judge whether its the last step or there is no more new city:
    if (step_count >= step_L) or (len(visited_city_list) >= city_n):
        # finish this branch
        visited_cities_num = len(visited_city_list)
        print('\t----' + str(step_count) + ', ' + str(visited_cities_num) + ', ' + str(max_visited_cities_num) + ', ' + str(current_city_id))
        # update max_visited_cities_num
        if (visited_cities_num>max_visited_cities_num):
            max_visited_cities_num=visited_cities_num
        return 0
    
    # find its children cities
    current_child_index_list = []
    for child_id in range(0, len(parent_id_list)):
        if parent_id_list[child_id] == current_city_id:
            current_child_index_list.append(child_id + 1)
    
    # find next step
    # whether it has children:
    if len(current_child_index_list) != 0:
        # iterate all children which are not in visited_city_list:
        #print('\t-' + str(current_city_id) + ', ' + str(current_child_index_list) + ', ' + str(step_count + 1))
        for child_id in current_child_index_list:
            if child_id not in visited_city_list:
                find_next_step(child_id, visited_city_list, parent_id_list, step_count+1)

    #whether it is the root city:
    if (current_city_id != 0):
        # goto to its parent again
        parent_id = parent_id_list[current_city_id - 1]
        #print('\t..' + str(current_city_id) + ', ' + str(parent_id) + ', ' + str(step_count + 1))
        find_next_step(parent_id, visited_city_list, parent_id_list, step_count + 1)
    return 0

if __name__ == "__main__":
    line_1_list = sys.stdin.readline().strip().split()
    city_n = int(line_1_list[0])
    step_L = int(line_1_list[1])
    
    line_2 = sys.stdin.readline().strip()
    parent_id_list = list(map(int, line_2.split()))
    
    visited_city_list = []
    max_visited_cities_num = 0
    
    current_city_id = 0
    step_count = 0
    find_next_step(current_city_id, visited_city_list, parent_id_list, step_count)
    print(max_visited_cities_num)
