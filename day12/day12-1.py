import collections

grid = []
with open("inputs/day12-data.txt", "r") as fp:
    for line in fp:
        grid.append(list(line.strip()))


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ROWS = len(grid)
COLUMNS = len(grid[0])


def bfs_area_and_perimeter(pos, grid):
    queue = collections.deque([pos])
    visited = set([pos])
    perimeter = 0
    while len(queue) > 0:
        row, column = queue.popleft()
        # Standalone cell
        perimeter += 4

        # Check cell below and remove 2, if it matches,
        # from perimeter since it will be a shared edge between 2
        # vertices removed
        if row + 1 < ROWS and grid[row + 1][column] == grid[row][column]:
            perimeter -= 2

        # Check cell to the right and remove 2, if it matches,
        # from perimeter since it will be a shared edge between 2
        # vertices removed
        if column + 1 < COLUMNS and grid[row][column + 1] == grid[row][column]:
            perimeter -= 2
        for row_change, column_change in DIRECTIONS:
            new_row = row + row_change
            new_column = column + column_change

            if (
                0 <= new_row < ROWS
                and 0 <= new_column < COLUMNS
                and (new_row, new_column) not in visited
                and grid[new_row][new_column] == grid[row][column]
            ):
                visited.add((new_row, new_column))
                queue.append((new_row, new_column))

    return (visited, perimeter)


price = 0
visited = set([])
for row in range(ROWS):
    for column in range(COLUMNS):
        if (row, column) not in visited:
            plant_region, perimeter = bfs_area_and_perimeter((row, column), grid)
            area = len(plant_region)
            visited = visited.union(plant_region)
            print(f"plant - {grid[row][column]}")
            print(f"area - {area}")
            print(f"perimeter - {perimeter}")
            print("\n\n")
            price += area * perimeter

print(f"price {price}")
