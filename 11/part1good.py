from typing import Self
from time import time

start = time()

memo: dict[int, dict[int, int]] = dict()
rocks: list[int] = list()

with open('input.txt') as file:
    rocks = [int(num) for num in file.read().split(' ')]


def rocks_from_blinks(number: int, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1
    if number == 0:
        return rocks_from_blinks(1, blinks_remaining-1)
    if number not in memo:
        memo[number] = dict()
    if blinks_remaining not in memo[number]:
        str_num = str(number)
        if len(str_num) % 2 == 0:
            memo[number][blinks_remaining] = rocks_from_blinks(int(str_num[len(
                str_num) // 2:]), blinks_remaining - 1) + rocks_from_blinks(int(str_num[:len(str_num) // 2]), blinks_remaining - 1)
        else:
            memo[number][blinks_remaining] = rocks_from_blinks(number * 2024, blinks_remaining - 1)
    return memo[number][blinks_remaining]


blinks: int = 75
rock_count: int = 0

for rock in rocks:
    rock_count += rocks_from_blinks(rock, blinks)

print(rock_count)
print(time() - start)
