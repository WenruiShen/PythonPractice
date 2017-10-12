def judge_equal(num_1, num_2):
    if (num_1 == num_2):
        return True
    else:
        return False

def judge_reback_list(input_list):
    list_len = len(input_list)
    cmp_n = int(list_len / 2)
    for i in range(0, cmp_n):
        if judge_equal(input_list[i], input_list[list_len - 1 - i]) is not True:
            # This list is not reback list.
            return False
    return True

def list_opt(ori_list):
    judge_reback_list = ori_list
    return judge_reback_list

def main_function():
    n = int(input())
    input_list = [int(x) for x in input().split()]
    if n != len(input_list):
        return
    
    
    reback_mark = judge_reback_list(input_list)
    if reback_mark is False:
        input_list = list_opt(input_list)
    
    print(len(input_list))
    return

main_function()