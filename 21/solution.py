num_button_locs: dict[str, tuple[int, int]] = {'7': (0, 0), '8': (0, 1), '9': (0, 2),
                                               '4': (1, 0), '5': (1, 1), '6': (1, 2),
                                               '1': (2, 0), '2': (2, 1), '3': (2, 2),
                                               '0': (3, 1), 'A': (3, 2)}
dir_button_locs: dict[str, tuple[int, int]] = {'^': (0, 1), 'A': (0, 2),
                                               '<': (1, 0), 'v': (1, 1), '>': (1, 2)}


def align_vertical(pos: list[int], dest: tuple[int, int]) -> str:
    directions: str = ''
    row_diff = dest[0] - pos[0]
    if row_diff < 0:
        directions += '^'*abs(row_diff)
    elif row_diff > 0:
        directions += 'v'*row_diff
    return directions


def align_horizontal(pos: list[int], dest: tuple[int, int]) -> str:
    directions: str = ''
    col_diff = dest[1] - pos[1]
    if col_diff > 0:
        directions += '>'*col_diff
    elif col_diff < 0:
        directions += '<'*abs(col_diff)
    return directions


def get_directions(code: str, numpad: bool) -> str:
    directions: str = ''
    if numpad:
        pos: list[int] = [num_button_locs['A'][0], num_button_locs['A'][1]]
    else:
        pos: list[int] = [dir_button_locs['A'][0], dir_button_locs['A'][1]]
    for key in code:
        dest = num_button_locs[key] if numpad else dir_button_locs[key]
        if (numpad and dest[1] != 0) or (dest[1] != 0 and not numpad):
            directions += align_horizontal(pos, dest)
            directions += align_vertical(pos, dest)
        else:
            directions += align_vertical(pos, dest)
            directions += align_horizontal(pos, dest)
        directions += 'A'
        pos[0] = dest[0]
        pos[1] = dest[1]
    return directions


complexity_sum = 0
with open('input.txt') as file:
    for line in file:
        code = line.rstrip('\n')
        directions = get_directions(code, True)
        directions = get_directions(directions, False)
        directions = get_directions(directions, False)
        complexity_sum += len(directions) * int(code[:3])

print('Part 1:', complexity_sum)