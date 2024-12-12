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


def get_trail_score(next: int, row: int, col: int) -> int:
    if next == 10:
        return 1
    score = 0
    if col < len(grid[row]) - 1 and grid[row][col+1] == next:
        score += get_trail_score(next+1, row, col+1)
    if col > 0 and grid[row][col-1] == next:
        score += get_trail_score(next+1, row, col-1)
    if row < len(grid) - 1 and grid[row+1][col] == next:
        score += get_trail_score(next+1, row+1, col)
    if row > 0 and grid[row-1][col] == next:
        score += get_trail_score(next+1, row-1, col)
    return score

total_trail_score = sum([get_trail_score(1, trailhead[0], trailhead[1]) for trailhead in trailheads])

print(total_trail_score)
