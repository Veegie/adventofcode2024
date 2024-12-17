from typing import Self, Optional
from collections import deque


class Direction:
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


class Cost:
    STRAIGHT = 1
    TURN = 1001


class Move:
    def __init__(self, moving_from: list[int], direction: Direction, move_cost: Cost, prev: Optional[Self]):
        self.pos = [moving_from[0] + direction[0],
                    moving_from[1] + direction[1]]
        self.direction = direction
        self.prev = prev
        if prev:
            self.cost = prev.cost + move_cost
        else:
            self.cost = move_cost


maze: list[list[str]] = list()
start_pos: list[int] = None
lowest_cost_to: dict[tuple, int] = dict()


with open('input.txt') as file:
    for row, line in enumerate(file):
        if not start_pos:
            s_loc = line.find('S')
            if s_loc > -1:
                start_pos = [row, s_loc]
        maze.append([char for char in line if char != '\n'])


def is_move_valid(move: Move) -> bool:
    move_loc = tuple(move.pos)
    if move_loc in lowest_cost_to and move.cost > lowest_cost_to[move_loc]:
        return False
    return True


def get_valid_moves(prev: Move | None) -> list[Move]:
    if not prev:
        dir = Direction.RIGHT
        pos = start_pos
    else:
        dir = prev.direction
        pos = prev.pos
    moves = []
    if dir != Direction.DOWN and maze[pos[0]-1][pos[1]] != '#':
        moves.append(Move(pos, Direction.UP, Cost.STRAIGHT if dir ==
                          Direction.UP else Cost.TURN, prev))
    if dir != Direction.LEFT and maze[pos[0]][pos[1]+1] != '#':
        moves.append(Move(pos, Direction.RIGHT, Cost.STRAIGHT if dir ==
                          Direction.RIGHT else Cost.TURN, prev))
    if dir != Direction.UP and maze[pos[0]+1][pos[1]] != '#':
        moves.append(Move(pos, Direction.DOWN, Cost.STRAIGHT if dir ==
                          Direction.DOWN else Cost.TURN, prev))
    if dir != Direction.RIGHT and maze[pos[0]][pos[1]-1] != '#':
        moves.append(Move(pos, Direction.LEFT, Cost.STRAIGHT if dir ==
                          Direction.LEFT else Cost.TURN, prev))
    return filter(is_move_valid, moves)

end_loc: tuple = None
queue: deque[Move] = deque()
queue.extend(get_valid_moves(None))
path_ends: list[Move] = list()
best_paths: set[tuple] = set()

while (len(queue) > 0):
    cur_move = queue.popleft()
    move_loc = tuple(cur_move.pos)
    if move_loc not in lowest_cost_to or cur_move.cost <= lowest_cost_to[move_loc]:
        lowest_cost_to[move_loc] = cur_move.cost
        if maze[cur_move.pos[0]][cur_move.pos[1]] == 'E':
            end_loc = move_loc
            path_ends.append(cur_move)
            continue
    queue.extend(get_valid_moves(cur_move))

for move in path_ends:
    if move.cost == lowest_cost_to[end_loc]:
        cur_move = move
        while cur_move.prev:
            best_paths.add(tuple(cur_move.pos))
            cur_move = cur_move.prev

print(len(best_paths)+2)
print(lowest_cost_to[end_loc])
