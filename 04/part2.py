grid: list[list[int]] = []
a_locs: list[list[int]] = []

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
    # all checked locations are guaranteed to be in range [1, len(grid[i])-1]
    seqs = 0
    # M on left
    if grid[i-1][j-1] == 1 and grid[i+1][j-1] == 1 and grid[i-1][j+1] == 3 and grid[i+1][j+1] == 3:
        seqs += 1
    # M on top
    elif grid[i-1][j-1] == 1 and grid[i+1][j-1] == 3 and grid[i-1][j+1] == 1 and grid[i+1][j+1] == 3:
        seqs += 1
    # M on right
    elif grid[i-1][j-1] == 3 and grid[i+1][j-1] == 3 and grid[i-1][j+1] == 1 and grid[i+1][j+1] == 1:
        seqs += 1
    # M on bottom
    elif grid[i-1][j-1] == 3 and grid[i+1][j-1] == 1 and grid[i-1][j+1] == 3 and grid[i+1][j+1] == 1:
        seqs += 1
    return seqs        

xmas_count: int = 0
with open('input.txt', 'r') as file:
    lines: list[str] = file.read().splitlines()
    for line_idx, line in enumerate(lines):
        grid_line: list[str] = []
        for char_idx, c in enumerate(line):
            char_val: int = enum(c)
            if char_val == 2 and line_idx in range(1, len(line) - 1) and char_idx in range(1, len(line) - 1):
                a_locs.append([line_idx, char_idx])
            grid_line.append(char_val)
        grid.append(grid_line)

for loc in a_locs:
    xmas_count += count_seqs(loc[0],loc[1])
              
print(xmas_count)
