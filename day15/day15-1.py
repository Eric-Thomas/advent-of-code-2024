grid = []
moves = []

parsing_grid = True
with open("inputs/day15-data.txt", "r") as fp:
    for line in fp:
        if line == "\n":
            parsing_grid = False
        elif parsing_grid:
            grid.append(list(line.strip()))
        else:
            moves += list(line.strip())


ROWS = len(grid)
COLUMNS = len(grid[0])


def can_move(robot_pos, grid, move):
    row, column = robot_pos
    if move == "^":
        row -= 1
        while row > 0:
            if grid[row][column] == ".":
                return True
            if grid[row][column] == "#":
                return False
            row -= 1
    elif move == "v":
        row += 1
        while row < ROWS:
            if grid[row][column] == ".":
                return True
            if grid[row][column] == "#":
                return False
            row += 1
    elif move == ">":
        column += 1
        while column < COLUMNS:
            if grid[row][column] == ".":
                return True
            if grid[row][column] == "#":
                return False
            column += 1
    elif move == "<":
        column -= 1
        while column < COLUMNS:
            if grid[row][column] == ".":
                return True
            if grid[row][column] == "#":
                return False
            column -= 1


def get_robot_pos(grid):
    for row in range(ROWS):
        for column in range(COLUMNS):
            if grid[row][column] == "@":
                return (row, column)


def get_amount_of_blocking_boxes(grid, robot_pos, move):
    row, column = robot_pos
    row_check = row
    column_check = column
    blocking_boxes = 0
    if move == "^":
        while row_check - 1 > 0 and grid[row_check - 1][column_check] == "O":
            blocking_boxes += 1
            row_check -= 1
    elif move == "v":
        while row_check + 1 > 0 and grid[row_check + 1][column_check] == "O":
            blocking_boxes += 1
            row_check += 1
    elif move == ">":
        while column_check + 1 > 0 and grid[row_check][column_check + 1] == "O":
            blocking_boxes += 1
            column_check += 1
    elif move == "<":
        while column_check - 1 > 0 and grid[row_check][column_check - 1] == "O":
            blocking_boxes += 1
            column_check -= 1

    return blocking_boxes


def get_updated_grid(grid, robot_pos, move):
    blocking_boxes = get_amount_of_blocking_boxes(grid, robot_pos, move)
    row, column = robot_pos
    if move == "^":
        grid[row][column] = "."
        grid[row - 1][column] = "@"
        if blocking_boxes > 0:
            grid[row - blocking_boxes - 1][column] = "O"
    elif move == "v":
        grid[row][column] = "."
        grid[row + 1][column] = "@"
        if blocking_boxes > 0:
            grid[row + blocking_boxes + 1][column] = "O"
    elif move == ">":
        grid[row][column] = "."
        grid[row][column + 1] = "@"
        if blocking_boxes > 0:
            grid[row][column + blocking_boxes + 1] = "O"
    elif move == "<":
        grid[row][column] = "."
        grid[row][column - 1] = "@"
        if blocking_boxes > 0:
            grid[row][column - blocking_boxes - 1] = "O"

    return grid


def get_updated_robot_pos(robot_pos, move):
    row, column = robot_pos
    if move == "^":
        return (row - 1, column)
    elif move == "v":
        return (row + 1, column)
    elif move == ">":
        return (row, column + 1)
    elif move == "<":
        return (row, column - 1)


robot_pos = get_robot_pos(grid)

for move in moves:
    if not can_move(robot_pos, grid, move):
        continue

    grid = get_updated_grid(grid, robot_pos, move)
    robot_pos = get_updated_robot_pos(robot_pos, move)

gps_sum = 0
for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column] == "O":
            gps_sum += (row * 100) + column

print(gps_sum)
