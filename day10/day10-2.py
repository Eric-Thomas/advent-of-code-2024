import collections

grid = []
with open("inputs/day10-data.txt") as fp:
    for line in fp:
        grid.append([int(char) for char in list(line.strip())])


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ROWS = len(grid)
COLUMNS = len(grid[0])


def bfs(pos):
    queue = collections.deque([pos])
    visited = set([pos])
    trailheads = 0
    while len(queue) > 0:
        row, column = queue.popleft()
        if grid[row][column] == 9:
            trailheads += 1
            continue
        for row_change, column_change in DIRECTIONS:
            new_row = row + row_change
            new_column = column + column_change
            if 0 <= new_row < ROWS and 0 <= new_column < COLUMNS and grid[new_row][new_column] == 1 + grid[row][column]:
                visited.add((new_row, new_column))
                queue.append((new_row, new_column))

    return trailheads


total_trailheads = 0
for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column] == 0:
            total_trailheads += bfs((row, column))

print(f"total trailheads {total_trailheads}")
