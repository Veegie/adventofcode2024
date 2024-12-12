import re
import time

start_time = time.time()
class Direction:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

obstacles: dict[tuple, bool] = dict()
loop_obstacles: dict[tuple, bool] = dict()
visited: dict[tuple, list[Direction]] = dict()

start_pos: tuple = None
grid_width = 0
grid_height = 0
with open('input.txt') as file:
    for line_num, line in enumerate(file):
        for loc in [(match.span()[0], line_num) for match in re.finditer('#', line)]:
            obstacles[loc] = True
        if not start_pos:
            start_pos_match: re.Match = re.search(r'\^', line)
            if start_pos_match:
                start_pos = (start_pos_match.start(), line_num)
        grid_height = line_num + 1
        grid_width = max(grid_width, len(line))

def move(cur_pos: tuple, dir: Direction) -> tuple:
    return (cur_pos[0] + dir[0], cur_pos[1] + dir[1])

def turn(direct: Direction) -> Direction:
    match(direct):
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP

def obstacle_creates_loop(loop_test_pos: tuple, dir: Direction) -> bool:
    loop_test_visited: dict[tuple, list[Direction]] = dict()
    while loop_test_pos[0] in range(0, grid_width) and loop_test_pos[1] in range(0, grid_height):
        if loop_test_pos not in loop_test_visited:
            loop_test_visited[loop_test_pos] = []
        loop_test_visited[loop_test_pos].append(dir)
        next = move(loop_test_pos, dir)
        while next in obstacles:
            dir = turn(dir)
            next = move(loop_test_pos, dir)
        if next in loop_test_visited and dir in loop_test_visited[next]:
            return True
        loop_test_pos = next
    return False

cur_direction = Direction.UP
cur_pos = (start_pos[0], start_pos[1])
while cur_pos[0] in range(0, grid_width) and cur_pos[1] in range(0, grid_height):
    if cur_pos not in visited:
        visited[cur_pos] = []
    visited[cur_pos].append(cur_direction)
    next = move(cur_pos, cur_direction)
    while next in obstacles:
        cur_direction = turn(cur_direction)
        next = move(cur_pos, cur_direction)
    if next[0] in range(0, grid_width) and next[1] in range(0, grid_height) and next not in loop_obstacles and next != start_pos:
        obstacles[next] = True
        if obstacle_creates_loop(start_pos, Direction.UP):
            loop_obstacles[next] = True
        del obstacles[next]
    cur_pos = next

print('Part 1: ', len(visited))
print('Part 2: ', len(loop_obstacles))

print(time.time() - start_time)