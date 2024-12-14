import re

lobby_width = 101
lobby_length = 103

class Robot:
    def __init__(self, pos: list[int], vel: tuple):
        self.pos = pos
        self.vel = vel
        pass
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % lobby_width
        if self.pos[0] < 0:
            self.pos[0] += lobby_width
        self.pos[1] = (self.pos[1] + self.vel[1]) % lobby_length
        if self.pos[1] < 0:
            self.pos[1] += lobby_length
    
    def __str__(self):
        return 'Pos: ' + str(self.pos)

robots: list[Robot] = list()

with open('input.txt') as file:
    for line in file:
        parts = re.split(' |=', line.rstrip('\n'))
        pos_str = parts[1].split(',')
        v_str = parts[3].split(',')
        robots.append(Robot([int(pos_str[0]), int(pos_str[1])], (int(v_str[0]),int(v_str[1]))))

for robot in robots:
    seconds = 100
    while seconds > 0:
        robot.update()
        seconds -= 1

q1, q2, q3, q4 = 0,0,0,0
midpoint_x = lobby_width // 2
midpoint_y = lobby_length // 2
for robot in robots:
    if robot.pos[0] in range(0,midpoint_x):
        if robot.pos[1] in range(0,midpoint_y):
            q1 += 1
        elif robot.pos[1] in range(midpoint_y + 1, lobby_length):
            q2 += 1
    elif robot.pos[0] in range(midpoint_x + 1, lobby_width):
        if robot.pos[1] in range(0,midpoint_y):
            q3 += 1
        elif robot.pos[1] in range(midpoint_y + 1, lobby_length):
            q4 += 1

print(q1*q2*q3*q4)

def all_unique(bots: list[Robot]) -> bool:
    positions: set[list[int]] = set()
    for robot in bots:
        pos = tuple(robot.pos)
        if pos in positions:
            return False
        positions.add(pos)
    return True

seconds = 100
while not all_unique(robots):
    for robot in robots:
        robot.update()
    seconds += 1

print(seconds)