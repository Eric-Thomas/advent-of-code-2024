import collections

grid = []
with open("inputs/day12-data.txt", "r") as fp:
    for line in fp:
        grid.append(list(line.strip()))


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
TOP_LEFT = (-1, -1)
TOP_RIGHT = (-1, 1)
BOTTOM_LEFT = (1, -1)
BOTTOM_RIGHT = (1, 1)
SEARCH_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
ROWS = len(grid)
COLUMNS = len(grid[0])

CORNER_PAIRS = [(UP, LEFT), (UP, RIGHT), (DOWN, LEFT), (DOWN, RIGHT)]
CONCAVE_CORNER_PAIR_TO_CORNERS = {
    (UP, LEFT): TOP_LEFT,
    (UP, RIGHT): TOP_RIGHT,
    (DOWN, LEFT): BOTTOM_LEFT,
    (DOWN, RIGHT): BOTTOM_RIGHT,
}


def bfs_corners(pos, grid):
    queue = collections.deque([pos])
    visited = set([pos])
    corners = 0
    while len(queue) > 0:
        row, column = queue.popleft()
        for corner_pair in CORNER_PAIRS:
            plants = 0
            for row_change, column_change in corner_pair:
                new_row = row + row_change
                new_column = column + column_change
                # X marks 1 part of the corner pair to search each iteration
                # We check whether X is the same plant or not
                # Xp represents a search position that is a plant
                # Just X represents a search position that is not the same plant
                # Xp would be plant A, but has been replace to illustrate
                # this search and what counts as a plant
                """
                    X       X
                   +-+-+-+---+
                 X |A Xp Xp A| X
                   +-+-+-+---+
                    X       X
                """
                if 0 <= new_row < ROWS and 0 <= new_column < COLUMNS and grid[new_row][new_column] == grid[row][column]:
                    plants += 1
            # convex corner if no plants in corner pair
            """
                X       X
            -> +-+-+-+---+ <-
             X |A Xp Xp A| X
            -> +-+-+-+---+ <-
                X       X
            """
            if plants == 0:
                corners += 1

            # concave corner if there are 2 plants in the corner pair
            # and no plant in the corner spot between them
            # C2 has 2 plants in the (UP, RIGHT) corner pair and
            # no plant in the TOP RIGHT diagonal so it counts a concave corner
            # Likewise C3 has 2 plants in the (LEFT, DOWN) search pair and
            # no plant in the bottom left diagonal so it counts a concave corner
            """
                 This is a concave corner
                  /
            +-+  /
            |C1|/
            + +-+
            |C2 C3|
            +-+   +
               |C4|
                +-+
            """
            if plants == 2:
                corner_row_change, corner_column_change = CONCAVE_CORNER_PAIR_TO_CORNERS[corner_pair]
                new_row = row + corner_row_change
                new_column = column + corner_column_change
                if 0 <= new_row < ROWS and 0 <= new_column < COLUMNS and grid[new_row][new_column] != grid[row][column]:
                    corners += 1

        for row_change, column_change in SEARCH_DIRECTIONS:
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

    return (visited, corners)


price = 0
visited = set([])
for row in range(ROWS):
    for column in range(COLUMNS):
        if (row, column) not in visited:
            plant_region, corners = bfs_corners((row, column), grid)
            area = len(plant_region)
            visited = visited.union(plant_region)
            print(f"plant - {grid[row][column]}")
            print(f"area - {area}")
            print(f"corners - {corners}")
            print("\n\n")
            price += area * corners

print(f"price {price}")
