import re

grid: list[list[int]] = []
x_locs: list[list[int]] = []

def enum(a: str) -> int:
    match a:
        case 'X':
            return 0
        case 'M':
            return 1
        case 'A':
            return 2
        case 'S':
            return 3
        case _:
            return -1

def count_seqs(i:int, j: int) -> int:
    seqs = 0
    # check up
    if i > 2:
        if grid[i-1][j] == 1 and grid[i-2][j] == 2 and grid[i-3][j] == 3:
            seqs += 1
        # check left
        if j > 2 and grid[i-1][j-1] == 1 and grid[i-2][j-2] == 2 and grid[i-3][j-3] == 3:
            seqs += 1
        # check right
        if j < len(grid[i]) - 3 and grid[i-1][j+1] == 1 and grid[i-2][j+2] == 2 and grid[i-3][j+3] == 3:
            seqs += 1
    # check down
    if i < len(grid) - 3:       
        if grid[i+1][j] == 1 and grid[i+2][j] == 2 and grid[i+3][j] == 3:
            seqs += 1
        # check left
        if j > 2 and grid[i+1][j-1] == 1 and grid[i+2][j-2] == 2 and grid[i+3][j-3] == 3:
            seqs += 1
        # check right
        if j < len(grid[i]) - 3 and grid[i+1][j+1] == 1 and grid[i+2][j+2] == 2 and grid[i+3][j+3] == 3:
            seqs += 1
    return seqs        

xmas_count: int = 0
with open('input.txt') as file:
    lines: list[str] = file.read().splitlines()
    for line_idx, line in enumerate(lines):
        xmas_count += len(re.findall('(?=XMAS|SAMX)', line))
        grid_line: list[str] = []
        for char_idx, c in enumerate(line):
            char_val: int = enum(c)
            if char_val == 0:
                x_locs.append([line_idx, char_idx])
            grid_line.append(char_val)
        grid.append(grid_line)

for loc in x_locs:
    xmas_count += count_seqs(loc[0],loc[1])
              
print(xmas_count)
