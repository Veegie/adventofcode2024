from typing import Self
import math
import heapq

grid_width: int = 71
grid_height: int = 71

class Direction:
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    EACH: list[Self] = [UP, RIGHT, DOWN, LEFT]

def opposite(direction: Direction) -> Direction:
    match(direction):
        case Direction.UP:
            return Direction.DOWN
        case Direction.RIGHT:
            return Direction.LEFT
        case Direction.DOWN:
            return Direction.UP
        case Direction.LEFT:
            return Direction.RIGHT

class Grid_Space:
    def __init__(self, pos: tuple[int, int]):
        self.pos = pos
        self.cost = math.inf
        self.moved_dir: Direction | None = None
    def __lt__(self, other: Self):
        return self.cost < other.cost

def solve(grid: list[list[str]]) -> tuple[set[tuple], int]:
    """
    Finds and returns a tuple specifying the coordinates of the tiles
    describing the shortest path from (0,0) to (grid_height,grid_width)
    in the specified grid. Returns (None, -1) if there is no possible path.
    """
    space_heap: list[Grid_Space] = []
    unvisited: dict[tuple,Grid_Space] = dict()
    visited: dict[tuple, Grid_Space] = dict()

    for i in range(grid_height):
        for j in range(grid_width):
            if grid[i][j] != '#':
                loc = (i,j)
                space = Grid_Space(loc)
                space_heap.append(space)
                unvisited[loc] = space
    
    space_heap[0].cost = 0
    heapq.heapify(space_heap)
    
    goal = (grid_height - 1, grid_width - 1)
    while len(space_heap) > 0:
        cur_space = heapq.heappop(space_heap)
        if cur_space.pos == goal:
            path: set[tuple] = set()
            cost = cur_space.cost
            loc: list[int] = [goal[0], goal[1]]
            while cur_space.moved_dir:
                back = opposite(cur_space.moved_dir)
                loc[0] += back[0]
                loc[1] += back[1]
                loc_tuple = tuple(loc)
                path.add(loc_tuple)
                cur_space = visited[loc_tuple]
            return (path, cost)
        if cur_space.cost == math.inf:
            return (None, -1)
        space_pos = tuple(cur_space.pos)
        visited[space_pos] = cur_space
        del unvisited[space_pos]
        for direction in Direction.EACH:
            move_loc = (cur_space.pos[0] + direction[0], cur_space.pos[1] + direction[1])
            if move_loc in unvisited and cur_space.cost + 1 < unvisited[move_loc].cost:
                unvisited[move_loc].cost = cur_space.cost + 1
                unvisited[move_loc].moved_dir = direction
        heapq.heapify(space_heap)
    return (None, -1)


grid: list[list[str]] = [['.']*grid_width for i in range(grid_height)]

solution: tuple[set[tuple], int] = None
with open('input.txt') as file:
    for line_num, line in enumerate(file):
        coords = line.rstrip('\n').split(',')
        grid[int(coords[0])][int(coords[1])] = '#'
        if line_num == 1023:
            solution = solve(grid)
            print('Part 1: ', solution[1])
        elif line_num > 1023:
            # Only re-solve if the best path is obstructed.
            if tuple([int(i) for i in coords]) in solution[0]:
                solution = solve(grid)
                if solution[1] == -1:
                    print('Part 2:', line.rstrip('\n'))
                    break
