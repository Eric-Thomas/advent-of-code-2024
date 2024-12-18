import heapq

grid = []
with open("inputs/day16-data.txt", "r") as fp:
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

heap = [(0, start, EAST)]
heapq.heapify(heap)
distances = {start: 0}
min_score = float("inf")
while len(heap) > 0:
    score, pos, prev_direction = heapq.heappop(heap)
    row, column = pos
    if grid[row][column] == "E":
        min_score = min(min_score, score)
        continue

    for direction in DIRECTIONS:
        row_change, column_change = direction
        new_row = row + row_change
        new_column = column + column_change
        if 0 <= new_row < ROWS and 0 <= new_column < COLUMNS and grid[new_row][new_column] in [".", "E"]:
            score_increase = 1
            if direction != prev_direction:
                score_increase += 1000
            if (new_row, new_column) not in distances or distances[(new_row, new_column)] > score + score_increase:
                heapq.heappush(heap, (score + score_increase, (new_row, new_column), direction))
                distances[((new_row, new_column))] = score + score_increase

print(min_score)
