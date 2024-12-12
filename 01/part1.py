list1, list2 = [], []

with open('input.txt') as file:
    for line in file:
        nums = line.split(None)
        list1.append(int(nums[0]))
        list2.append(int(nums[1]))

list1.sort()
list2.sort()

sum_difference = 0
for i in range(len(list1)):
    sum_difference += abs(list2[i] - list1[i])

print(sum_difference)