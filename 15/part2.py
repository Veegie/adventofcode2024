class Direction:
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


cur_pos: list[int] = None
next_step: list[int] = [-1, -1]
push_to: list[int] = [-1, -1]
grid: list[list[str]] = list()


def move_horizontal(dir: Direction, steps: int) -> None:
    for _ in range(0, steps):
        next_step[0] = cur_pos[0]
        next_step[1] = cur_pos[1] + dir[1]
        if grid[next_step[0]][next_step[1]] == '#':
            return
        elif grid[next_step[0]][next_step[1]] == '[' or grid[next_step[0]][next_step[1]] == ']':
            push_to[0] = next_step[0]
            push_to[1] = next_step[1] + dir[1]
            while grid[push_to[0]][push_to[1]] == '[' or grid[push_to[0]][push_to[1]] == ']':
                push_to[1] += dir[1]
            if grid[push_to[0]][push_to[1]] == '#':
                return
            if dir[1] > 0:
                while push_to[1] > next_step[1]:
                    grid[push_to[0]][push_to[1]] = ']'
                    grid[push_to[0]][push_to[1]-1] = '['
                    push_to[1] -= 2
            else:
                while push_to[1] < next_step[1]:
                    grid[push_to[0]][push_to[1]] = '['
                    grid[push_to[0]][push_to[1]+1] = ']'
                    push_to[1] += 2
            grid[next_step[0]][next_step[1]] = '.'
        cur_pos[0] = next_step[0]
        cur_pos[1] = next_step[1]


def get_pushable_boxes(dir: Direction, boxes: list[list[int]]) -> list[list[int]]:
    next_level: list[int] = []
    for box in boxes:
        if grid[box[0]+dir[0]][box[1]] == '#' or grid[box[0]+dir[0]][box[1]+1] == '#':
            return []
        if grid[box[0]+dir[0]][box[1]] == '[' and [box[0]+dir[0],box[1]] not in next_level:
            next_level.append([box[0]+dir[0],box[1]])
        if grid[box[0]+dir[0]][box[1]] == ']' and [box[0]+dir[0],box[1]-1] not in next_level:
            next_level.append([box[0]+dir[0],box[1]-1])
        if grid[box[0]+dir[0]][box[1]+1] == '[' and [box[0]+dir[0],box[1]+1] not in next_level:
            next_level.append([box[0]+dir[0],box[1]+1])
    if len(next_level) == 0:
        return boxes
    pushable_next = get_pushable_boxes(dir, next_level)
    if len(pushable_next) < len(next_level):
        return []
    boxes += pushable_next
    return boxes


def move_vertical(dir: Direction, steps: int) -> None:
    for _ in range(0, steps):
        next_step[0] = cur_pos[0] + dir[0]
        next_step[1] = cur_pos[1]
        if grid[next_step[0]][next_step[1]] == '#':
            return
        elif grid[next_step[0]][next_step[1]] == '[' or grid[next_step[0]][next_step[1]] == ']':
            boxes_to_push: list[list[int]] = list()
            if grid[next_step[0]][next_step[1]] == '[':
                boxes_to_push = get_pushable_boxes(dir, [[next_step[0],next_step[1]]])
            else:
                boxes_to_push = get_pushable_boxes(dir, [[next_step[0],next_step[1]-1]])
            
            if len(boxes_to_push) == 0:
                return
            
            boxes_to_push.reverse()
            for box in boxes_to_push:
                grid[box[0]+dir[0]][box[1]] = '['
                grid[box[0]+dir[0]][box[1]+1] = ']'
                grid[box[0]][box[1]] = '.'
                grid[box[0]][box[1]+1] = '.'

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
                    cur_pos = [row, start_col*2]
            cur_row = ''
            for char in line.rstrip('\n'):
                if char == 'O':
                    cur_row += '[]'
                elif char == '@':
                    cur_row += '@.'
                elif char == '#':
                    cur_row += '##'
                elif char == '.':
                    cur_row += '..'
            grid.append([char for char in cur_row])
        else:
            move_str += line.rstrip('\n')

i: int = 0
steps: int = 0
direction: Direction = Direction.UP
while i < len(move_str):
    steps = 1
    while i < len(move_str) - 1 and move_str[i+1] == move_str[i]:
        steps += 1
        i += 1
    match(move_str[i]):
        case '^':
            direction = Direction.UP
            move_vertical(direction, steps)
        case '>':
            direction = Direction.RIGHT
            move_horizontal(direction, steps)
        case 'v':
            direction = Direction.DOWN
            move_vertical(direction, steps)
        case '<':
            direction = Direction.LEFT
            move_horizontal(direction, steps)
    i += 1

coord_sum = 0
for i in range(0, len(grid)):
    for j in range(0, len(grid[i])):
        if grid[i][j] == '[':
            coord_sum += 100 * i + j

print(coord_sum)