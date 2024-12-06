import time
import concurrent.futures
import threading
from typing import List
import copy

grid: List[List[str]] = []
guard_start_pos = None
with open("inputs/day6-data.txt") as fp:
    for row, line in enumerate(fp):
        line = line.strip()
        grid.append([])
        for column, char in enumerate(line):
            if char == "^":
                guard_start_pos = (row, column)
                # Replace guard with "." so we don't have to keep track of ^ character
                char = "."
            grid[row].append(char)


def get_next_pos(pos, direction):
    row, column = pos

    if direction == "up":
        return (row - 1, column)
    elif direction == "down":
        return (row + 1, column)
    elif direction == "left":
        return (row, column - 1)
    elif direction == "right":
        return (row, column + 1)

    raise ValueError(f"direction must be in ['up', 'down', 'left', 'right']")


def rotate(direction):
    if direction == "up":
        return "right"
    elif direction == "right":
        return "down"
    elif direction == "down":
        return "left"
    elif direction == "left":
        return "up"
    raise ValueError(f"direction must be in ['up', 'down', 'left', 'right']")


def pos_in_original_grid(grid, guard_pos):
    positions_visited = set([guard_pos])
    direction = "up"
    while True:
        next_pos = get_next_pos(guard_pos, direction)
        row, column = next_pos
        if row < 0 or row >= len(grid) or column < 0 or column >= len(grid[0]):
            print("Guard left the room")
            print(f"Positions visited {len(positions_visited)}")
            return positions_visited
        if grid[row][column] == "#":
            direction = rotate(direction)
        elif grid[row][column] == ".":
            positions_visited.add(next_pos)
            guard_pos = next_pos


def guard_walk(new_obstical_pos, grid):
    grid[new_obstical_pos[0]][new_obstical_pos[1]] = "#"
    global positions_that_cause_loop
    guard_pos = guard_start_pos
    direction = "up"
    positions_and_directions_visited = set([(guard_pos, direction)])
    while True:
        next_pos = get_next_pos(guard_pos, direction)
        if (next_pos, direction) in positions_and_directions_visited:
            print("Guard stuck in loop!")
            return 1
        row, column = next_pos
        if row < 0 or row >= len(grid) or column < 0 or column >= len(grid[0]):
            print("Guard left the room")
            return 0
        if grid[row][column] == "#":
            direction = rotate(direction)
        elif grid[row][column] == ".":
            positions_and_directions_visited.add((next_pos, direction))
            guard_pos = next_pos


def process_function(row, column, grid, guard_start_pos, valid_obstruction_positions):
    if (
        (row, column) in valid_obstruction_positions
        and (row, column) != guard_start_pos
        and grid[row][column] == "."
    ):
        grid_copy = copy.deepcopy(grid)
        return guard_walk((row, column), grid_copy)
    return 0


def thread_function(grid, guard_start_pos, valid_obstruction_positions):
    ROWS = len(grid)
    COLS = len(grid[0])
    positions_that_cause_loop = 0

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for row in range(ROWS):
            for column in range(COLS):
                futures.append(
                    executor.submit(
                        process_function,
                        row,
                        column,
                        grid,
                        guard_start_pos,
                        valid_obstruction_positions,
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            try:
                positions_that_cause_loop += future.result()
            except Exception as e:
                print(f"Task raised an exception: {e}")

    return positions_that_cause_loop


valid_obstruction_positions = pos_in_original_grid(grid, guard_start_pos)
start_time = time.time()
positions_that_cause_loop = thread_function(
    grid, guard_start_pos, valid_obstruction_positions
)
print(f"Positions that caused a loop: {positions_that_cause_loop}")
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time)
