# -*- coding:utf-8 -*-  
###############################################################################
# 寻找丑数
#
# Wenrui.Shen
# Thomas.shen3904@qq.com
# 2017/09/12
###############################################################################
import sys 

def delet_ele(recent_ug, x1):
    while True:
        if (recent_ug > x1):
            break
        elif (recent_ug % x1 == 0):
            recent_ug = recent_ug / x1
        else:
            break
    return recent_ug

def judge_zhishu(recent_ug):
    res_mark = False
    if recent_ug > 1:
        for i in range(2,recent_ug):
            if (recent_ug % i) == 0:
                break
            else:
                res_mark = True
    return res_mark
    
def get_next_ug(recent_ug):
    while True:
        recent_ug = recent_ug + 1
        temp_ug = recent_ug
        temp_ug = delet_ele(temp_ug, 2)
        temp_ug = delet_ele(temp_ug, 3)
        temp_ug = delet_ele(temp_ug, 5)
        if judge_zhishu(temp_ug):
            break
    return recent_ug

for line in sys.stdin:
    input_list = line.split()
    n_str = input_list[0]
    n_int = int(n_str)

    i=2
    ug_count = 1
    recent_ug = 1
    
    if n_int > 1:
        while True:
            if n_int > ug_count:
                recent_ug = get_next_ug(recent_ug)
                ug_count = ug_count + 1
            else:
                # find Nth ug_num:
                break
    print(recent_ug)