def can_equate(goal_total: int, partial_total: int, nums: list[int], start_index: int) -> bool:
    if start_index == len(nums):
        return goal_total == partial_total
    elif partial_total > goal_total:
        return False
    return can_equate(goal_total, partial_total + nums[start_index], nums, start_index + 1) or can_equate(goal_total, partial_total * nums[start_index], nums, start_index + 1)


calibration_result_sum = 0
with open('input.txt') as file:
    for line in file:
        equation: list[str] = line.split(': ')
        total: int = int(equation[0])
        parts: list[int] = [int(val) for val in equation[1].split(' ')]
        if can_equate(total, parts[0], parts, 1):
            calibration_result_sum += total

print(calibration_result_sum)
