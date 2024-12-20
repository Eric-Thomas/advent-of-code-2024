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

PICOSECONDS_SAVED_THRESHOLD = 75
PICSOSECONDS_CHEAT_THRESHOLD = 20


def bfs_cheat(start, positions_to_step_count):
    queue = collections.deque([start])
    visited = set([start])
    cheat_start_and_end_to_picoseconds_saved = {}
    steps = 1
    while len(queue) > 0 and steps < PICSOSECONDS_CHEAT_THRESHOLD:
        queue_len = len(queue)
        for _ in range(queue_len):
            row, column = queue.popleft()
            for row_change, column_change in DIRECTIONS:
                new_row = row + row_change
                new_column = column + column_change
                if 0 <= new_row < ROWS and 0 <= new_column < COLUMNS and (new_row, new_column) not in visited:
                    # Don't add . to queue bc cheats should only go through walls until last step of a .
                    if grid[new_row][new_column] == "#":
                        visited.add((new_row, new_column))
                        queue.append((new_row, new_column))
                    # We've found a . ending our cheat so compare it and see if we saved anything
                    elif (
                        steps >= 2
                        and (new_row, new_column) in positions_to_step_count
                        and positions_to_step_count[(new_row, new_column)] - positions_to_step_count[start] > steps
                    ):
                        cheat_start_and_end_to_picoseconds_saved[(start, (new_row, new_column))] = (
                            positions_to_step_count[(new_row, new_column)]
                        )
                        -positions_to_step_count[start]
        steps += 1

    return cheat_start_and_end_to_picoseconds_saved


total_steps = len(positions_to_step_count)
cheat_start_and_end_to_picoseconds_saved = {}
for pos in positions_to_step_count:
    cheat_start_and_end_to_picoseconds_saved.update(bfs_cheat(pos, positions_to_step_count))

cheats_over_threshold = 0
for picoseconds_saved in cheat_start_and_end_to_picoseconds_saved.values():
    if picoseconds_saved > PICOSECONDS_SAVED_THRESHOLD:
        cheats_over_threshold += 1

print(cheat_start_and_end_to_picoseconds_saved)
print(cheats_over_threshold)
print(positions_to_step_count)
