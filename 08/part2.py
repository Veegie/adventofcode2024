antennae: dict[str, list[tuple]] = dict()

grid_height = 0
grid_width = 0
antinode_locs: set[tuple] = set()
filename = 'input.txt'
with open(filename) as file:
    for line in file:
        grid_width = len(line)
        grid_height += 1

with open(filename) as file:
    for y, line in enumerate(file):
        for x, char in enumerate(line):
            if char == '.' or char == '\n':
                continue
            if char not in antennae:
                antennae[char] = []
            else:
                antinode_locs.add((y,x))
            for other_antenna in antennae[char]:
                antinode_locs.add((other_antenna[0], other_antenna[1]))
                y_dist = y-other_antenna[0]
                x_dist = abs(x-other_antenna[1])
                upper_antinode_y = other_antenna[0] - y_dist
                lower_antinode_y = y + y_dist
                if x > other_antenna[1]:
                    left_antinode_x = other_antenna[1] - x_dist
                    right_antinode_x = x + x_dist
                else:
                    left_antinode_x = x - x_dist
                    right_antinode_x = other_antenna[1] + x_dist
                while upper_antinode_y >= 0 or lower_antinode_y < grid_height:
                    if upper_antinode_y >= 0:
                        if x > other_antenna[1] and left_antinode_x >= 0:
                            antinode_locs.add((upper_antinode_y, left_antinode_x))
                        elif x <= other_antenna[1] and right_antinode_x < grid_width:
                            antinode_locs.add((upper_antinode_y, right_antinode_x))
                        upper_antinode_y -= y_dist
                    if lower_antinode_y < grid_width:
                        if x < other_antenna[1] and left_antinode_x >= 0:
                            antinode_locs.add((lower_antinode_y, left_antinode_x))
                        elif x >= other_antenna[1] and right_antinode_x < grid_width:
                            antinode_locs.add((lower_antinode_y, right_antinode_x))
                        lower_antinode_y += y_dist
                    left_antinode_x -= x_dist
                    right_antinode_x += x_dist
            antennae[char].append((y, x))

print(len(antinode_locs))
