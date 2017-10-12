import sys


def judge_num(num):
    if(num % 7 == 0):
        return 1
    else:
        return 0

def judge_two_num(first_num, second_num):
    str_num = '' + str(first_num) + str(second_num)
    new_num = int(str_num)
    return judge_num(new_num)





input_n = int(sys.stdin.readline().strip().split()[0])
num_list = list(map(int, sys.stdin.readline().strip().split()))

i = 0
count_sum = 0
for first_num in num_list:
    if (i >= len(num_list)-1):
        break
    i = i + 1
    for second_num in num_list[i:]:
        res_1 = judge_two_num(first_num, second_num)
        res_2 = judge_two_num(second_num, first_num)
        count_sum = count_sum + res_1 + res_2

print(count_sum)

#print(input_n)
#print(len(num_list))