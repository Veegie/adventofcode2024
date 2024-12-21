from typing import Self

maze: list[list[int]] = list()
start_pos = tuple[int, int]
end_pos = tuple[int, int]


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
    QUADRANTS: list[Self] = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def enumerate_maze(maze: list[list[int]], start_pos: tuple, end_pos: tuple) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = list()
    cur_pos: list[int] = [start_pos[0], start_pos[1]]
    path.append(tuple(cur_pos))
    step_count = 1
    while cur_pos[0] != end_pos[0] or cur_pos[1] != end_pos[1]:
        maze[cur_pos[0]][cur_pos[1]] = step_count
        for dir in Direction.CARDINAL:
            if maze[cur_pos[0]+dir[0]][cur_pos[1]+dir[1]] == 0:
                cur_pos[0] += dir[0]
                cur_pos[1] += dir[1]
                path.append(tuple(cur_pos))
                step_count += 1
                break
    maze[cur_pos[0]][cur_pos[1]] = step_count
    return path


def good_cheat_count(pos: tuple[int, int], threshold: int) -> int:
    good_cheats = 0
    cur_val = maze[pos[0]][pos[1]]
    for dir in Direction.CARDINAL:
        if maze[pos[0]+dir[0]][pos[1]+dir[1]] == -1 and pos[0]+dir[0]*2 in range(0, len(maze)) and pos[1]+dir[1]*2 in range(0, len(maze[pos[0]])):
            next_val = maze[pos[0]+dir[0]*2][pos[1]+dir[1]*2]
            if next_val > 0 and next_val - cur_val > threshold:
                good_cheats += 1
    return good_cheats


def good_cheat_count_radial(pos: tuple[int, int], threshold: int, radius: int) -> int:
    good_cheats = 0
    cur_val = maze[pos[0]][pos[1]]
    for i in range(radius, 0, -1):
        for dir in Direction.CARDINAL:
            if pos[0] + i*dir[0] in range(0, len(maze)) and pos[1] + i*dir[1] in range(0, len(maze[pos[0]])):
                next_val = maze[pos[0] + i*dir[0]][pos[1] + i*dir[1]]
                if next_val > 0 and next_val - cur_val >= threshold + i:
                    good_cheats += 1
        for j in range(radius-i, 0, -1):
            for dir in Direction.QUADRANTS:
                if pos[0] + i*dir[0] in range(0, len(maze)) and pos[1] + j*dir[1] in range(0, len(maze[pos[0]])):
                    next_val = maze[pos[0] + i*dir[0]][pos[1] + j*dir[1]]
                    if next_val > 0 and next_val - cur_val >= threshold + i + j:
                        good_cheats += 1
    return good_cheats


with open('input.txt') as file:
    for row, line in enumerate(file):
        maze_row: list[int] = [0]*len(line.rstrip('\n'))
        maze.append(maze_row)
        for col, char in enumerate(line.rstrip('\n')):
            if char == '#':
                maze[row][col] = -1
            elif char == 'S':
                start_pos = (row, col)
            elif char == 'E':
                end_pos = (row, col)

path = enumerate_maze(maze, start_pos, end_pos)

good_cheats = 0
good_cheats_radial = 0
for step in path:
    good_cheats += good_cheat_count(step, 100)
    good_cheats_radial += good_cheat_count_radial(step, 100, 20)

print('Part 1:', good_cheats)
print('Part 2:', good_cheats_radial)
