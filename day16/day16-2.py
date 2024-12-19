import heapq
from collections import defaultdict, deque

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
        if grid[row][column] == "E":
            end = (row, column)

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


heap = [(0, start, EAST)]
scores = defaultdict(lambda: float("inf"))
scores[(start, EAST)] = 0
prev_tiles = defaultdict(set)
min_score = float("inf")

while len(heap) > 0:
    score, pos, prev_direction = heapq.heappop(heap)
    row, column = pos

    if score > min_score:
        continue

    if grid[row][column] == "E":
        min_score = min(min_score, score)
        continue

    for direction in DIRECTIONS:
        row_change, column_change = direction
        new_row, new_column = row + row_change, column + column_change

        if 0 <= new_row < ROWS and 0 <= new_column < COLUMNS and grid[new_row][new_column] in [".", "E"]:
            score_increase = 1
            if direction != prev_direction:
                score_increase += 1000
            new_score = score + score_increase

            if new_score < scores[((new_row, new_column), direction)]:
                scores[((new_row, new_column), direction)] = new_score
                heapq.heappush(heap, (new_score, (new_row, new_column), direction))
                prev_tiles[((new_row, new_column), direction)] = {(pos, prev_direction)}

            elif new_score == scores[((new_row, new_column), direction)]:
                prev_tiles[((new_row, new_column), direction)].add((pos, prev_direction))


best_paths = set()
queue = deque([(end, d) for d in DIRECTIONS if (end, d) in scores and scores[(end, d)] == min_score])

while queue:
    tile, direction = queue.popleft()
    best_paths.add(tile)

    for prev_tile, prev_direction in prev_tiles[(tile, direction)]:
        if prev_tile not in best_paths:
            queue.append((prev_tile, prev_direction))

print(len(best_paths))
