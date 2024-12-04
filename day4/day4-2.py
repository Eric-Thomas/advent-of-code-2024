grid = []
with open("inputs/day4-data.txt") as fp:
    for line in fp:
        grid.append(list(line.strip()))


ROWS = len(grid)
COLUMNS = len(grid[0])

TOP_LEFT_TO_BOTTOM_RIGHT_DIRECTIONS = [(-1, -1), (1, 1)]
TOP_RIGHT_TO_BOTTOM_LEFT_DIRECTIONS = [(-1, 1), (1, -1)]
X_MAS_CORNER_VALUES = {"M", "S"}


def in_bounds(row, column):
    return 0 <= row < ROWS and 0 <= column < COLUMNS


def is_x_mas(pos, grid):
    row, column = pos
    top_left_to_bottom_right = set()
    for row_change, column_change in TOP_LEFT_TO_BOTTOM_RIGHT_DIRECTIONS:
        if in_bounds(row + row_change, column + column_change):
            top_left_to_bottom_right.add(grid[row + row_change][column + column_change])

    if top_left_to_bottom_right != X_MAS_CORNER_VALUES:
        return False

    top_right_to_bottom_left = set()
    for row_change, column_change in TOP_RIGHT_TO_BOTTOM_LEFT_DIRECTIONS:
        if in_bounds(row + row_change, column + column_change):
            top_right_to_bottom_left.add(grid[row + row_change][column + column_change])

    if top_right_to_bottom_left != X_MAS_CORNER_VALUES:
        return False

    return True


matches = 0
for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column] == "A":
            if is_x_mas((row, column), grid):
                matches += 1


print(matches)
