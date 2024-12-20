import collections
import copy

grid = []
with open("inputs/day20-data.txt", "r") as fp:
    for line in fp:
        grid.append(list(line.strip()))


ROWS = len(grid)
COLUMNS = len(grid[0])

for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column] == "S":
            start = (row, column)

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

queue = collections.deque([[start, set([start]), 0]])
visited = set([start])
positions_to_step_count = {start: 0}
best_path = None
while len(queue) > 0:
    pos, prev_posisitions, step = queue.popleft()
    row, column = pos
    if grid[row][column] == "E":
        best_path = prev_posisitions
        break

    for direction in DIRECTIONS:
        row_change, column_change = direction
        new_row = row + row_change
        new_column = column + column_change
        if (
            0 <= new_row < ROWS
            and 0 <= new_column < COLUMNS
            and grid[new_row][new_column] in [".", "E"]
            and (new_row, new_column) not in visited
        ):
            prev_positions_copy = copy.deepcopy(prev_posisitions)
            prev_positions_copy.add((new_row, new_column))
            visited.add((new_row, new_column))
            positions_to_step_count[(new_row, new_column)] = step + 1
            queue.append([(new_row, new_column), prev_positions_copy, step + 1])

PICOSECONDS_SAVED_THRESHOLD = 63

total_steps = len(positions_to_step_count)
best_cheat_move_diff = float("-inf")
best_cheat_move = None
cheats_over_threshold = 0
for pos, step in positions_to_step_count.items():
    row, column = pos
    for row_change, column_change in DIRECTIONS:
        new_row_wall = row + row_change
        new_column_wall = column + column_change
        new_row_path = row + 2 * row_change
        new_column_path = column + 2 * column_change

        if (
            0 <= new_row_wall < ROWS
            and 0 <= new_column_wall < COLUMNS
            and grid[new_row_wall][new_column_wall] == "#"
            and (new_row_path, new_column_path) in positions_to_step_count
        ):
            if positions_to_step_count[(new_row_path, new_column_path)] - step > PICOSECONDS_SAVED_THRESHOLD:
                best_cheat_move_diff = positions_to_step_count[(new_row_path, new_column_path)] - step
                best_cheat_move = [(row, column), ((new_row_path, new_column_path))]
                cheats_over_threshold += 1

print(cheats_over_threshold)
