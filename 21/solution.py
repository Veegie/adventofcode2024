from functools import cache
from itertools import permutations

n: dict[str, tuple[int, int]] = {'7': (0, 0), '8': (0, 1), '9': (0, 2),
                                 '4': (1, 0), '5': (1, 1), '6': (1, 2),
                                 '1': (2, 0), '2': (2, 1), '3': (2, 2),
                                 '':  (3, 0), '0': (3, 1), 'A': (3, 2)}
d: dict[str, tuple[int, int]] = {'':  (0, 0), '^': (0, 1), 'A': (0, 2),
                                 '<': (1, 0), 'v': (1, 1), '>': (1, 2)}


@cache
def get_all_paths(numpad: bool, start: str, end: str) -> list[str]:
    start_pos = n[start] if numpad else d[start]
    end_pos = n[end] if numpad else d[end]
    col_diff = end_pos[1] - start_pos[1]
    row_diff = end_pos[0] - start_pos[0]

    if col_diff < 0:
        col_chars = '<'*abs(col_diff)
    else:
        col_chars = '>'*col_diff

    if row_diff < 0:
        row_chars = '^'*abs(row_diff)
    else:
        row_chars = 'v'*row_diff

    if col_diff == 0:
        return [row_chars]
    elif row_diff == 0:
        return [col_chars]

    directions = [''.join(p) for p in permutations(row_chars+col_chars)]
    if numpad:
        if start_pos[1] == 0 and end_pos[0] == 3:
            if start_pos[0] == 0:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('vvv'), directions)]
            elif start_pos[0] == 1:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('vv'), directions)]
            elif start_pos[0] == 2:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('v'), directions)]
        if start_pos[0] == 3 and end_pos[1] == 0:
            if start_pos[1] == 1:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('<'), directions)]
            elif start_pos[1] == 2:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('<<'), directions)]
    else:
        if start_pos == (1, 0) and end_pos[0] == 0:
            directions = [direction for direction in filter(
                lambda d: not d.startswith('^'), directions)]
        if start_pos[0] == 0 and end_pos[1] == 0:
            if start_pos[1] == 1:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('<'), directions)]
            elif start_pos[1] == 2:
                directions = [direction for direction in filter(
                    lambda d: not d.startswith('<<'), directions)]
    return directions


@cache
def shortest_path(numpad: bool, code: str, robots: int) -> int:
    if robots == 0:
        return len(code)

    min_length = 0
    cur_char = 'A'
    for key in code:
        key_paths = set(get_all_paths(numpad, cur_char, key))
        path_lengths = [shortest_path(False, path + 'A', robots-1)
                        for path in key_paths]
        min_length += min(path_lengths)
        cur_char = key
    return min_length


complexity_sum = 0
complexity_sum_p2 = 0
with open('input.txt') as file:
    for line in file:
        code = line.rstrip('\n')
        complexity_sum += shortest_path(True, code, 3) * int(code[:3])
        complexity_sum_p2 += shortest_path(True, code, 26) * int(code[:3])

print('Part 1:', complexity_sum)
print('Part 2:', complexity_sum_p2)
