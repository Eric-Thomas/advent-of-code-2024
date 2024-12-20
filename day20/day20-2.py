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

queue = collections.deque([start])
visited = set([start])
tiles_walked = [start]
while len(queue) > 0:
    pos = queue.popleft()
    row, column = pos
    if grid[row][column] == "E":
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
            visited.add((new_row, new_column))
            tiles_walked.append((new_row, new_column))
            queue.append((new_row, new_column))

PICOSECONDS_SAVED_THRESHOLD = 100
PICSOSECONDS_CHEAT_THRESHOLD = 20


def get_manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


cheats_to_picoseconds_saved_over_threshold = {}
for step, pos in enumerate(tiles_walked):
    for step2 in range(step + 1, len(tiles_walked)):
        pos2 = tiles_walked[step2]
        cheat_distance = get_manhattan_distance(pos, pos2)
        if (
            pos != pos2
            and cheat_distance <= PICSOSECONDS_CHEAT_THRESHOLD
            and step2 - step - cheat_distance >= PICOSECONDS_SAVED_THRESHOLD
        ):
            cheats_to_picoseconds_saved_over_threshold[(pos, pos2)] = step2 - step - cheat_distance

print(len(cheats_to_picoseconds_saved_over_threshold))
