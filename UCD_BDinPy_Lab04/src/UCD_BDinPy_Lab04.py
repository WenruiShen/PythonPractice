import sys

# Big Data in Python- Lab-04 Task-1
'''
def read_file(file_name):
    numbers = set()
    fin = open(file_name, "r")
    for line in fin.readlines():
        line = line.strip()
        num = int(line)
        numbers.add(num)
    fin.close()
    return numbers

numbers1 = read_file(sys.argv[1])
numbers2 = read_file(sys.argv[2])
print(numbers1.intersection(numbers2))
'''
# Big Data in Python- Lab-04 Task-2
if len(sys.argv) < 3:
    print("Must Input more than 2 numbers!")
    sys.exit()

line_numbers = []
