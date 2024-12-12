from typing import Self
from time import time

start = time()
class Node:
    val: str
    next: Self

    def __init__(self, val: str):
        self.val = val
        self.next = None

    def __str__(self):
        res = self.val
        n = self.next
        while n:
            res += ' -> ' + n.val
            n = n.next
        return res

    def split(self) -> None:
        temp = self.next
        self.next = Node(str(int(self.val[len(self.val) // 2:])))
        self.val = str(int(self.val[:len(self.val) // 2]))
        self.next.next = temp


rock_list: Node = None
cur_node: Node = None
rock_count: int = 0
memo: dict[int, dict[int,int]] = dict()

with open('input.txt') as file:
    rocks = file.read().split(' ')
    rock_count = len(rocks)
    rock_list = Node(rocks[0])
    cur_node = rock_list
    for i in range(1, len(rocks)):
        cur_node.next = Node(rocks[i])
        cur_node = cur_node.next


def rocks_from_blinks(digit: int, blinks_remaining: int) -> int:
    if digit not in memo:
        memo[digit] = dict()
    if blinks_remaining not in memo[digit]:
        if blinks_remaining < 2:
            return 0
        if digit > 4:
            if blinks_remaining < 3:
                return 0
            elif blinks_remaining == 3:
                return 1
            elif blinks_remaining == 4:
                return 3
            else:
                val_split = str(digit * 4096576)
                if digit == 8:
                    digits = [int(d) for d in val_split]
                    memo[digit][blinks_remaining] = 6
                    memo[digit][blinks_remaining] += rocks_from_blinks(digits[-1], blinks_remaining - 4)
                    for i in range(0, len(val_split) - 2):
                        memo[digit][blinks_remaining] += rocks_from_blinks(digits[i], blinks_remaining - 5)
                else:
                    memo[digit][blinks_remaining] = 7 + sum([rocks_from_blinks(int(d), blinks_remaining - 5) for d in val_split]) 
        elif digit > 0:
            if blinks_remaining == 2:
                return 1
            elif blinks_remaining == 3 or blinks_remaining == 4:
                return 3
            else:
                val = digit * 2024
                memo[digit][blinks_remaining] = 3 + sum([rocks_from_blinks(int(d), blinks_remaining - 3) for d in str(val)])
        else:
            if blinks_remaining < 3:
                return 0
            elif blinks_remaining == 3:
                return 1
            elif blinks_remaining == 4:
                return 3
            else:
                val = 2024
                memo[digit][blinks_remaining] = 3 + sum([rocks_from_blinks(int(d), blinks_remaining - 4) for d in str(val)])
    return memo[digit][blinks_remaining]
            

blinks: int = 75
while blinks > 0 and rock_list:
    cur_node = rock_list
    prev = None
    split_rocks: list[Node] = list()
    while cur_node:
        if len(cur_node.val) == 1:
            rock_count += rocks_from_blinks(int(cur_node.val), blinks)
            if prev:
                prev.next = cur_node.next
            else:
                rock_list = cur_node.next
        elif len(cur_node.val) % 2 == 0:
            split_rocks.append(cur_node)
            prev = cur_node
        else:
            cur_node.val = str(int(cur_node.val) * 2024)
            prev = cur_node
        cur_node = cur_node.next
    for rock in split_rocks:
        rock.split()
        rock_count += 1
    blinks -= 1

print(rock_count)
print(time() - start)