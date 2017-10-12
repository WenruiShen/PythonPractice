# -*- coding:utf-8 -*-  
###############################################################################
# 动态规划问题解答：
# 已有面值为2^k,其中k为非负整数,的硬币各两个，例如当k为3时，拥有硬币：{1,1,2,2,4,4,8,8}。
# 现需要支付n元，问共有多少种支付方案？
#
# Wenrui.Shen
# Thomas.shen3904@qq.com
# 2017/09/14
###############################################################################
import sys
import copy

def find_max_k(n):
    max_k = 0
    for k in range(n, -1, -1):
        #print(k)
        max_k = k
        max_value = 2**k
        if max_value <= n:
            break
    return max_k

def select_coin(input_n, max_k, sum_num_methods, selected_k_dic):
    temp_selected_k_dic = copy.deepcopy(selected_k_dic)# Python使用深拷贝实现字典的备份
    for k_i in range(max_k, -1, -1):
        #print('******' + str(input_n) + ',' + str(max_k) + ',' + str(k_i))
        selected_k_dic = copy.deepcopy(temp_selected_k_dic)
        select_k_coin_num = selected_k_dic.get(k_i)
        if select_k_coin_num is None:
            selected_k_dic[k_i]=0
        if selected_k_dic[k_i] < 2:
            coin_value = 2**k_i
            rest_money = input_n - coin_value
            if rest_money > 0:
                #print("--" + str(coin_value))
                selected_k_dic[                 k_i] = selected_k_dic[k_i]+1
                sum_num_methods = select_coin(rest_money, k_i, sum_num_methods, selected_k_dic)
            elif rest_money == 0:
                #print("--" + str(coin_value))
                selected_k_dic[k_i] = selected_k_dic[k_i]+1
                sum_num_methods = sum_num_methods + 1
                print(selected_k_dic)
                continue
            elif rest_money < 0:
                #print('***********')
                continue
        else:
            continue
    
    return sum_num_methods

selected_k_dic = {}
sum_num_methods = 0
input_n = int(input().split()[0])
#input_n = 6
max_k = find_max_k(input_n)
print('Input n is :' + str(input_n))
sum_num_methods = select_coin(input_n, max_k, sum_num_methods, selected_k_dic)
#sum_num_methods = find_max_k(input_n)
print(sum_num_methods)