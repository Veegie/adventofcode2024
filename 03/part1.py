import re

sum = 0
with open('input.txt') as file:
    for line in file:
        for mul in re.findall(r'(?<=mul\()\d+,\d+(?=\))', line):
            ops = mul.split(',')
            sum += int(ops[0]) * int(ops[1])
            
print(sum)