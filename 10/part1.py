trailheads: list[tuple] = []
grid: list[list[int]] = []
with open('input.txt') as file:
    for row_num, line in enumerate(file):
        grid_row = []
        for col_num, char in enumerate(line):
            if char == '\n':
                continue
            elif char == '.':
                grid_row.append(char)
            else:
                if char == '0':
                    trailheads.append((row_num, col_num))
                grid_row.append(int(char))
        grid.append(grid_row)

total_trail_score = 0
for trailhead in trailheads:
    peaks: set[tuple] = set()
    path: list[tuple] = [trailhead]
    while len(path) > 0:
        step = path.pop()
        row = step[0]
        col = step[1]
        if grid[row][col] == 9:
            peaks.add((row, col))
        next = grid[row][col] + 1
        if col < len(grid[row]) - 1 and grid[row][col+1] == next:
            path.append((row, col+1))
        if col > 0 and grid[row][col-1] == next:
            path.append((row, col-1))
        if row < len(grid) - 1 and grid[row+1][col] == next:
            path.append((row+1, col))
        if row > 0 and grid[row-1][col] == next:
            path.append((row-1, col))
    total_trail_score += len(peaks)

print(total_trail_score)
