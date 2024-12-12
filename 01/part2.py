list1 = []
list_two_dict = dict()

with open('1-input.txt') as file:
    for line in file:
        nums = line.split(None)
        list1.append(int(nums[0]))
        second_num = int(nums[1])
        if second_num in list_two_dict:
            list_two_dict[second_num] += 1
        else:
            list_two_dict[second_num] = 1

similarity = 0
for i in range(len(list1)):
    if list1[i] in list_two_dict:
        similarity += list1[i] * list_two_dict[list1[i]]

print(similarity)