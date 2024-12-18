from collections import deque

ROWS = 71
COLUMNS = 71
grid = []
for row in range(ROWS):
    grid.append(["."] * COLUMNS)

bytes_pos = []
with open("inputs/day18-data.txt", "r") as fp:
    for line in fp:
        x, y = line.strip().split(",")
        bytes_pos.append((int(x), int(y)))


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def bfs(grid):
    visited = set((0, 0))
    queue = deque([(0, 0)])
    steps = 0
    while len(queue) > 0:
        queue_len = len(queue)
        for _ in range(queue_len):
            row, column = queue.popleft()
            if row == ROWS - 1 and column == COLUMNS - 1:
                return steps

            for row_change, column_change in DIRECTIONS:
                new_row = row + row_change
                new_column = column + column_change
                if (
                    0 <= new_row < ROWS
                    and 0 <= new_column < COLUMNS
                    and (new_row, new_column) not in visited
                    and grid[new_row][new_column] == "."
                ):
                    visited.add((new_row, new_column))
                    queue.append((new_row, new_column))
        steps += 1


for bytes_fallen in range(len(bytes_pos)):
    row, column = bytes_pos[bytes_fallen]
    grid[row][column] = "#"
    if bfs(grid) is None:
        print(f"{row},{column}")
        break
