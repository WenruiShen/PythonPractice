# -*- coding:utf-8 -*-  
import sys 

'''
Count the number of a given date, like (Year, month, day)

1990 9 20
2000 5 1

263
122
'''
def is_run_year(year):  
    return ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0)  
    pass

def date_count(year, month, day):  
    daycount = 0  
    monthnum = 1  
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  
    run_month_day = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if is_run_year(year):  
        for i in run_month_day:  
            if monthnum < month:
                daycount = daycount + i
                monthnum = monthnum + 1
        daycount += day
        return daycount  
    else:  
        for i in month_day:  
            if monthnum < month:  
                daycount = daycount + i  
                monthnum = monthnum + 1
        daycount += day
        return daycount

day_seq_list = []
for line in sys.stdin:
    input_list = line.split()
    year = int(input_list[0])
    month = int(input_list[1])
    day = int(input_list[2])
    day_num = date_count(year, month, day)
    print(day_num)
    day_seq_list.append(day_num)



#for day_seq in day_seq_list:
#    print(day_seq)

