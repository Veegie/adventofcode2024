class Direction:
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


cur_pos: list[int] = None
next_step: list[int] = [-1, -1]
push_to: list[int] = [-1, -1]
grid: list[list[str]] = list()


def move(dir: Direction, steps: int) -> None:
    for _ in range(0, steps):
        next_step[0] = cur_pos[0] + dir[0]
        next_step[1] = cur_pos[1] + dir[1]
        if grid[next_step[0]][next_step[1]] == '#':
            return
        elif grid[next_step[0]][next_step[1]] == 'O':
            push_to[0] = next_step[0] + dir[0]
            push_to[1] = next_step[1] + dir[1]
            while grid[push_to[0]][push_to[1]] == 'O':
                push_to[0] += dir[0]
                push_to[1] += dir[1]
            if grid[push_to[0]][push_to[1]] == '#':
                return
            grid[push_to[0]][push_to[1]] = 'O'
            grid[next_step[0]][next_step[1]] = '.'
        cur_pos[0] = next_step[0]
        cur_pos[1] = next_step[1]


move_str: str = ''
reading_room = True
with open('input.txt') as file:
    for row, line in enumerate(file):
        if len(line) == 1:
            reading_room = False
            continue
        if reading_room:
            if not cur_pos:
                start_col = line.find('@')
                if start_col > -1:
                    cur_pos = [row, start_col]
            cur_row = [c for c in line.rstrip('\n')]
            grid.append(cur_row)
        else:
            move_str += line.rstrip('\n')

i: int = 0
steps: int = 0
direction: Direction = Direction.UP
while i < len(move_str):
    steps = 1
    match(move_str[i]):
        case '^':
            direction = Direction.UP
        case '>':
            direction = Direction.RIGHT
        case 'v':
            direction = Direction.DOWN
        case '<':
            direction = Direction.LEFT
    while i < len(move_str) - 1 and move_str[i+1] == move_str[i]:
        steps += 1
        i += 1
    move(direction, steps)
    i += 1

coord_sum = 0
for i in range(0, len(grid)):
    for j in range(0, len(grid[i])):
        if grid[i][j] == 'O':
            coord_sum += 100 * i + j

print(coord_sum)