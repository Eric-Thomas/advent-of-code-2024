from typing import List, Optional

grid = []
moves = []

parsing_grid = True
with open("inputs/day15-data.txt", "r") as fp:
    for line in fp:
        row = []
        if line == "\n":
            parsing_grid = False
        elif parsing_grid:
            for char in line.strip():
                if char == "#":
                    row.append("#")
                    row.append("#")
                elif char == "O":
                    row.append("[")
                    row.append("]")
                elif char == ".":
                    row.append(".")
                    row.append(".")
                elif char == "@":
                    row.append("@")
                    row.append(".")
            grid.append(row)
        else:
            moves += list(line.strip())


ROWS = len(grid)
COLUMNS = len(grid[0])


def can_move_left_right(robot_pos, grid, move):
    row, column = robot_pos
    if move == ">":
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


def get_amount_of_blocking_left_right_boxes(grid, robot_pos, move):
    row, column = robot_pos
    row_check = row
    column_check = column
    blocking_boxes = 0
    if move == ">":
        while column_check + 1 > 0 and grid[row_check][column_check + 1] in ["[", "]"]:
            blocking_boxes += 0.5
            column_check += 1
    elif move == "<":
        while column_check - 1 > 0 and grid[row_check][column_check - 1] in ["[", "]"]:
            blocking_boxes += 0.5
            column_check -= 1

    return int(blocking_boxes)


def get_updated_grid_left_right(grid, robot_pos, move):
    row, column = robot_pos
    if move == ">":
        blocking_boxes = get_amount_of_blocking_left_right_boxes(grid, robot_pos, move)
        grid[row][column] = "."
        grid[row][column + 1] = "@"
        if blocking_boxes > 0:
            current_column = column + 2
            while grid[row][current_column] in ["[", "]"]:
                if grid[row][current_column] == "[":
                    grid[row][current_column] = "]"
                elif grid[row][current_column] == "]":
                    grid[row][current_column] = "["
                current_column += 1

            grid[row][current_column] = "]"
    elif move == "<":
        blocking_boxes = get_amount_of_blocking_left_right_boxes(grid, robot_pos, move)
        grid[row][column] = "."
        grid[row][column - 1] = "@"
        if blocking_boxes > 0:
            current_column = column - 2
            while grid[row][current_column] in ["[", "]"]:
                if grid[row][current_column] == "[":
                    grid[row][current_column] = "]"
                elif grid[row][current_column] == "]":
                    grid[row][current_column] = "["
                current_column -= 1

            grid[row][current_column] = "["

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


def box_can_move_up_down(box_left_pos, box_right_pos, grid, move) -> bool:
    left_side_can_move = True
    right_side_can_move = True
    box_left_row, box_left_column = box_left_pos
    box_right_row, box_right_column = box_right_pos
    if move == "^":
        if grid[box_left_row - 1][box_left_column] == "#" or grid[box_right_row - 1][box_right_column] == "#":
            return False
        if grid[box_left_row - 1][box_left_column] == "[":
            left_side_can_move = box_can_move_up_down(
                (box_left_row - 1, box_left_column), (box_right_row - 1, box_right_column), grid, move
            )
        if grid[box_left_row - 1][box_left_column] == "]":
            left_side_can_move = box_can_move_up_down(
                (box_left_row - 1, box_left_column - 1), (box_right_row - 1, box_right_column - 1), grid, move
            )
        if grid[box_right_row - 1][box_right_column] == "[":
            right_side_can_move = box_can_move_up_down(
                (box_left_row - 1, box_left_column + 1), (box_right_row - 1, box_right_column + 1), grid, move
            )
        if grid[box_right_row - 1][box_right_column] == "]":
            right_side_can_move = box_can_move_up_down(
                (box_left_row - 1, box_left_column), (box_right_row - 1, box_right_column), grid, move
            )
    elif move == "v":
        if grid[box_left_row + 1][box_left_column] == "#" or grid[box_right_row + 1][box_right_column] == "#":
            return False
        if grid[box_left_row + 1][box_left_column] == "[":
            left_side_can_move = box_can_move_up_down(
                (box_left_row + 1, box_left_column), (box_right_row + 1, box_right_column), grid, move
            )
        if grid[box_left_row + 1][box_left_column] == "]":
            left_side_can_move = box_can_move_up_down(
                (box_left_row + 1, box_left_column - 1), (box_right_row + 1, box_right_column - 1), grid, move
            )
        if grid[box_right_row + 1][box_right_column] == "[":
            right_side_can_move = box_can_move_up_down(
                (box_left_row + 1, box_left_column + 1), (box_right_row + 1, box_right_column + 1), grid, move
            )
        if grid[box_right_row + 1][box_right_column] == "]":
            right_side_can_move = box_can_move_up_down(
                (box_left_row + 1, box_left_column), (box_right_row + 1, box_right_column), grid, move
            )

    return left_side_can_move and right_side_can_move


def move_box_up_down(box_left_pos, box_right_pos, grid, move):
    box_left_row, box_left_column = box_left_pos
    box_right_row, box_right_column = box_right_pos
    if move == "^":
        if grid[box_left_row - 1][box_left_column] == "[":
            grid = move_box_up_down(
                (box_left_row - 1, box_left_column), (box_right_row - 1, box_right_column), grid, move
            )
        if grid[box_left_row - 1][box_left_column] == "]":
            grid = move_box_up_down(
                (box_left_row - 1, box_left_column - 1), (box_right_row - 1, box_right_column - 1), grid, move
            )
        if grid[box_right_row - 1][box_right_column] == "[":
            grid = move_box_up_down(
                (box_left_row - 1, box_left_column + 1), (box_right_row - 1, box_right_column + 1), grid, move
            )
        if grid[box_right_row - 1][box_right_column] == "]":
            grid = move_box_up_down(
                (box_left_row - 1, box_left_column), (box_right_row - 1, box_right_column), grid, move
            )

        # All boxes above are moved so we can move this one
        grid[box_left_row - 1][box_left_column] = "["
        grid[box_right_row - 1][box_right_column] = "]"
        grid[box_left_row][box_left_column] = "."
        grid[box_right_row][box_right_column] = "."
        return grid
    if move == "v":
        if grid[box_left_row + 1][box_left_column] == "[":
            grid = move_box_up_down(
                (box_left_row + 1, box_left_column), (box_right_row + 1, box_right_column), grid, move
            )
        if grid[box_left_row + 1][box_left_column] == "]":
            grid = move_box_up_down(
                (box_left_row + 1, box_left_column - 1), (box_right_row + 1, box_right_column - 1), grid, move
            )
        if grid[box_right_row + 1][box_right_column] == "[":
            grid = move_box_up_down(
                (box_left_row + 1, box_left_column + 1), (box_right_row + 1, box_right_column + 1), grid, move
            )
        if grid[box_right_row + 1][box_right_column] == "]":
            grid = move_box_up_down(
                (box_left_row + 1, box_left_column), (box_right_row + 1, box_right_column), grid, move
            )

        # All boxes below are moved so we can move this one
        grid[box_left_row + 1][box_left_column] = "["
        grid[box_right_row + 1][box_right_column] = "]"
        grid[box_left_row][box_left_column] = "."
        grid[box_right_row][box_right_column] = "."
        return grid


def get_updated_grid_up_down(robot_pos, grid, move) -> Optional[List[List[str]]]:
    """Will return updated grid if it is possible.
    If it is not possible, it will return None"""
    row, column = robot_pos
    if move == "^":
        if grid[row - 1][column] == "#":
            return None
        if grid[row - 1][column] == "[":
            if not box_can_move_up_down((row - 1, column), (row - 1, column + 1), grid, move):
                return None

            grid = move_box_up_down((row - 1, column), (row - 1, column + 1), grid, move)
        elif grid[row - 1][column] == "]":
            if not box_can_move_up_down((row - 1, column - 1), (row - 1, column), grid, move):
                return None

            grid = move_box_up_down((row - 1, column - 1), (row - 1, column), grid, move)

        grid[row][column] = "."
        grid[row - 1][column] = "@"
    elif move == "v":
        if grid[row + 1][column] == "#":
            return None
        if grid[row + 1][column] == "[":
            if not box_can_move_up_down((row + 1, column), (row + 1, column + 1), grid, move):
                return None
            grid = move_box_up_down((row + 1, column), (row + 1, column + 1), grid, move)
        elif grid[row + 1][column] == "]":
            if not box_can_move_up_down((row + 1, column - 1), (row + 1, column), grid, move):
                return None
            grid = move_box_up_down((row + 1, column - 1), (row + 1, column), grid, move)
        grid[row][column] = "."
        grid[row + 1][column] = "@"
    return grid


robot_pos = get_robot_pos(grid)


for move in moves:
    if move in ["<", ">"]:
        if can_move_left_right(robot_pos, grid, move):
            grid = get_updated_grid_left_right(grid, robot_pos, move)
            robot_pos = get_updated_robot_pos(robot_pos, move)
    elif move in ["^", "v"]:
        possible_valid_grid = get_updated_grid_up_down(robot_pos, grid, move)
        if possible_valid_grid:
            grid = possible_valid_grid
            robot_pos = get_updated_robot_pos(robot_pos, move)


gps_sum = 0
for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column] == "[":
            gps_sum += (row * 100) + column

print(gps_sum)

for row in range(ROWS):
    print("".join(grid[row]))
