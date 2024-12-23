from collections import deque
from itertools import permutations
from math import inf

n: dict[str, tuple[int, int]] = {'7': (0, 0), '8': (0, 1), '9': (0, 2),
                                 '4': (1, 0), '5': (1, 1), '6': (1, 2),
                                 '1': (2, 0), '2': (2, 1), '3': (2, 2),
                                 '0': (3, 1), 'A': (3, 2)}
d: dict[str, tuple[int, int]] = {'^': (0, 1), 'A': (0, 2),
                                 '<': (1, 0), 'v': (1, 1), '>': (1, 2)}

bot_dirs: dict[tuple[tuple[int, int], str], str] = {
    (d['A'], 'A'): 'A',
    (d['A'], '<'): 'v<<A',
    (d['A'], 'v'): 'v<A',
    (d['A'], '>'): 'vA',
    (d['A'], '^'): '<A',
    (d['<'], 'A'): '>>^A',
    (d['<'], '<'): 'A',
    (d['<'], 'v'): '>A',
    (d['<'], '>'): '>>A',
    (d['<'], '^'): '>^A',
    (d['v'], 'A'): '^>A',
    (d['v'], '<'): '<A',
    (d['v'], 'v'): 'A',
    (d['v'], '>'): '>A',
    (d['v'], '^'): '^A',
    (d['>'], 'A'): '^A',
    (d['>'], '<'): '<<A',
    (d['>'], 'v'): '<A',
    (d['>'], '>'): 'A',
    (d['>'], '^'): '^<A',
    (d['^'], 'A'): '>A',
    (d['^'], '<'): 'v<A',
    (d['^'], 'v'): 'vA',
    (d['^'], '>'): 'v>A',
    (d['^'], '^'): 'A', }


def numpad_dirs(start: str, end: str) -> list[str]:
    start_pos = n[start]
    end_pos = n[end]
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
    if start_pos[1] == 0 and end_pos[0] == 3:
        if start_pos[0] == 0:
            directions = [direction for direction in filter(lambda d: not d.startswith('vvv'), directions)]
        elif start_pos[0] == 1:
            directions = [direction for direction in filter(lambda d: not d.startswith('vv'), directions)]
        elif start_pos[0] == 2:
            directions = [direction for direction in filter(lambda d: not d.startswith('v'), directions)]
    if start_pos[0] == 3 and end_pos[1] == 0:
        if start_pos[1] == 1:
            directions = [direction for direction in filter(lambda d: not d.startswith('<'), directions)]
        elif start_pos[1] == 2:
            directions = [direction for direction in filter(lambda d: not d.startswith('<<'), directions)]
    return directions

def len_human_from_directional(input:str, extra_iterations: int, shortest_len: int) -> int:
    human_dirs_len = 0
    prev_char_at_layer: dict[int, str] = dict()
    for c in input:
        command = c
        for i in range(1+extra_iterations):
            transformed_command = ''
            if i not in prev_char_at_layer:
                prev_char_at_layer[i] = 'A'
            for r in command:
                transformed_command += bot_dirs[(d[prev_char_at_layer[i]], r)]
                prev_char_at_layer[i] = r
            command = transformed_command
        human_dirs_len += len(command)
        if human_dirs_len > shortest_len:
            return inf
    return human_dirs_len


def shortest_path(code: str, extra_iterations: int) -> int:
    code_paths = deque(numpad_dirs('A', code[0]))
    cur_char = code[0]
    for i in range(1,len(code)):
        numpad_directions = numpad_dirs(cur_char, code[i])
        for _ in range(len(code_paths)):
            partial_path = code_paths.popleft()
            for path in numpad_directions:
                code_paths.append(partial_path + 'A' + path)
        cur_char = code[i]
    path_set = set(code_paths)
    shortest_len = inf
    for path in path_set:
        human_dirs_len = len_human_from_directional(path + 'A', extra_iterations, shortest_len)
        if human_dirs_len < shortest_len:
            shortest_len = human_dirs_len
    return shortest_len

complexity_sum = 0
complexity_sum_p2 = 0
with open('input.txt') as file:
    for line in file:
        code = line.rstrip('\n')
        complexity_sum += shortest_path(code, 1) * int(code[:3])
        # Exponential time?
        # complexity_sum_p2 += shortest_path(code, 24) * int(code[:3])

print('Part 1:', complexity_sum)
print('Part 2:', complexity_sum_p2)
