from typing import Self

region_dict: dict[tuple, int] = dict()
areas: dict[int, int] = dict()
fence_sizes: dict[int, int] = dict()
side_count: dict[int, int] = dict()
first_tile: dict[int, tuple] = dict()
garden: list[list[str]] = list()


class Direction:
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)
    CARDINAL: list[Self] = [UP, RIGHT, DOWN, LEFT]
    OMNI: list[Self] = [UP, RIGHT, DOWN, LEFT,
                        UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


with open('input.txt') as file:
    lines = file.readlines()
    for line in lines:
        garden.append([c for c in line if c != "\n"])


def expand_region(row: int, col: int, char: str, region_num: int) -> None:
    if (row, col) in region_dict:
        return
    region_dict[(row, col)] = region_num
    areas[region_num] += 1
    for dir in Direction.CARDINAL:
        can_expand = True
        next_row = row + dir[0]
        next_col = col + dir[1]
        if next_row not in range(0, len(garden)) or garden[next_row][col] != char:
            fence_sizes[region_num] += 1
            can_expand = False
        if next_col not in range(0, len(garden[row])) or garden[row][next_col] != char:
            fence_sizes[region_num] += 1
            can_expand = False
        if can_expand:
            expand_region(row + dir[0], col + dir[1], char, region_num)


def is_in_garden(row: int, col: int) -> bool:
    return row in range(0, len(garden)) and col in range(0, len(garden[row]))


def can_move_to(row: int, col: int, char: str) -> bool:
    if not is_in_garden(row, col):
        return False
    if garden[row][col] != char:
        return False
    return True


def count_external_sides(row: int, col: int, char: str) -> int:
    sides = 1
    cur_direction = Direction.RIGHT
    start_row = row
    start_col = col
    while row != start_row or col != start_col or cur_direction != Direction.UP:
        if cur_direction == Direction.LEFT and can_move_to(row+1, col, char):
            cur_direction = Direction.DOWN
            sides += 1
        elif cur_direction == Direction.DOWN and can_move_to(row, col+1, char):
            cur_direction = Direction.RIGHT
            sides += 1
        elif cur_direction == Direction.UP and can_move_to(row, col-1, char):
            cur_direction = Direction.LEFT
            sides += 1
        elif cur_direction == Direction.RIGHT and can_move_to(row-1, col, char):
            cur_direction = Direction.UP
            sides += 1
        while not can_move_to(row + cur_direction[0], col + cur_direction[1], char):
            match(cur_direction):
                case Direction.UP:
                    cur_direction = Direction.RIGHT
                case Direction.RIGHT:
                    cur_direction = Direction.DOWN
                case Direction.DOWN:
                    cur_direction = Direction.LEFT
                case Direction.LEFT:
                    cur_direction = Direction.UP
            sides += 1
            if row == start_row and col == start_col and cur_direction == Direction.UP:
                return sides
        row += cur_direction[0]
        col += cur_direction[1]
    return sides


def get_encompassing_region(inner_region: int, row: int, col: int) -> int:
    char = garden[row][col]
    start_row = row
    start_col = col
    cur_direction = Direction.RIGHT
    encompassing_region = None
    while row != start_row or col != start_col or cur_direction != Direction.UP:
        for dir in Direction.OMNI:
            check_row = row + dir[0]
            check_col = col + dir[1]
            if not is_in_garden(check_row, check_col):
                return -1
            if region_dict[(check_row, check_col)] != inner_region:
                if encompassing_region == None:
                    encompassing_region = region_dict[(check_row, check_col)]
                elif encompassing_region != region_dict[(check_row, check_col)]:
                    return -1
        if cur_direction == Direction.LEFT and can_move_to(row+1, col, char):
            cur_direction = Direction.DOWN
        elif cur_direction == Direction.DOWN and can_move_to(row, col+1, char):
            cur_direction = Direction.RIGHT
        elif cur_direction == Direction.UP and can_move_to(row, col-1, char):
            cur_direction = Direction.LEFT
        elif cur_direction == Direction.RIGHT and can_move_to(row-1, col, char):
            cur_direction = Direction.UP
        while not can_move_to(row + cur_direction[0], col + cur_direction[1], char):
            match(cur_direction):
                case Direction.UP:
                    cur_direction = Direction.RIGHT
                case Direction.RIGHT:
                    cur_direction = Direction.DOWN
                case Direction.DOWN:
                    cur_direction = Direction.LEFT
                case Direction.LEFT:
                    cur_direction = Direction.UP
            if row == start_row and col == start_col and cur_direction == Direction.UP:
                if encompassing_region == None:
                    return -1
                return encompassing_region
        row += cur_direction[0]
        col += cur_direction[1]
    return encompassing_region


cur_region = 0
for i in range(0, len(garden)):
    for j in range(0, len(garden[i])):
        if (i, j) not in region_dict:
            areas[cur_region] = 0
            fence_sizes[cur_region] = 0
            side_count[cur_region] = 0
            first_tile[cur_region] = (i, j)
            expand_region(i, j, garden[i][j], cur_region)
            side_count[cur_region] += count_external_sides(i, j, garden[i][j])
            cur_region += 1

total_cost = 0
for i in range(0, cur_region):
    total_cost += fence_sizes[i] * areas[i]
    encompassing_region = get_encompassing_region(
        i, first_tile[i][0], first_tile[i][1])
    if encompassing_region != -1:
        side_count[encompassing_region] += side_count[i]

total_cost_with_discount = 0
for i in range(0, cur_region):
    total_cost_with_discount += areas[i] * side_count[i]

print('Part 1 cost:', total_cost)
print('Part 2 cost:', total_cost_with_discount)
