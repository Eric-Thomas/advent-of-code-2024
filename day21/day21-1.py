from collections import deque
from copy import deepcopy

DOOR_KEY_PAD = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
DOOR_KEY_PAD_ROWS = len(DOOR_KEY_PAD)
DOOR_KEY_PAD_COLUMNS = len(DOOR_KEY_PAD[0])
DIRECTIONAL_KEY_PAD = [[None, "^", "A"], ["<", "v", ">"]]
DIRECTIONAL_KEY_PAD_ROWS = len(DIRECTIONAL_KEY_PAD)
DIRECTIONAL_KEY_PAD_COLUMNS = len(DIRECTIONAL_KEY_PAD[0])

# After a lot of different combos, this directions ordering somehow works for the input
# Not sure if just lucky or there is some proof
DIRECTIONS = [(1, 0), (0, -1), (0, 1), (-1, 0)]


def get_door_key_pad_activate_pos():
    for row in range(DOOR_KEY_PAD_ROWS):
        for column in range(DOOR_KEY_PAD_COLUMNS):
            if DOOR_KEY_PAD[row][column] == "A":
                return (row, column)


def get_directional_key_pad_activate_pos():
    for row in range(DIRECTIONAL_KEY_PAD_ROWS):
        for column in range(DIRECTIONAL_KEY_PAD_COLUMNS):
            if DIRECTIONAL_KEY_PAD[row][column] == "A":
                return (row, column)


def door_code_button_to_pos(button):
    for row in range(DOOR_KEY_PAD_ROWS):
        for column in range(DOOR_KEY_PAD_COLUMNS):
            if DOOR_KEY_PAD[row][column] == button:
                return (row, column)

    raise ValueError(f"button {button} doesn't exist")


def directional_button_to_pos(button):
    for row in range(DIRECTIONAL_KEY_PAD_ROWS):
        for column in range(DIRECTIONAL_KEY_PAD_COLUMNS):
            if DIRECTIONAL_KEY_PAD[row][column] == button:
                return (row, column)

    raise ValueError(f"button {button} doesn't exist")


def direction_to_key_pad_button(direction):
    if direction == (0, 1):
        return ">"
    elif direction == (0, -1):
        return "<"
    elif direction == (1, 0):
        return "v"
    elif direction == (-1, 0):
        return "^"

    raise ValueError(f"direction {direction} doesn't exist")


def get_best_key_preses_to_door_key_pad_target(pos, target):
    all_key_presses = get_all_key_presses_to_door_key_pad_target(pos, target)
    key_presses_to_turns = {}
    for i in range(len(all_key_presses)):
        key_presses = all_key_presses[i]
        prev_key_press = key_presses[0]
        turns = 0
        for j in range(1, len(key_presses)):
            if key_presses[j] != prev_key_press:
                turns += 1
            prev_key_press = key_presses[j]

        key_presses_to_turns[i] = turns

    min_turns = min(key_presses_to_turns.values())
    best_key_presses = []
    for key_presses_index, turns in key_presses_to_turns.items():
        if turns == min_turns:
            best_key_presses.append(all_key_presses[key_presses_index])

    # Might need to return all of these and find the min somehow
    return best_key_presses[0]


def get_all_key_presses_to_door_key_pad_target(pos, target):
    queue = deque([(pos, [], set([pos]))])
    solutions = []
    while len(queue) > 0:
        pos, directions, prev_cells = queue.popleft()
        row, column = pos
        if DOOR_KEY_PAD[row][column] == target:
            solutions.append([direction_to_key_pad_button(direction) for direction in directions])

        for row_change, column_change in DIRECTIONS:
            new_row = row + row_change
            new_column = column + column_change
            if (
                0 <= new_row < DOOR_KEY_PAD_ROWS
                and 0 <= new_column < DOOR_KEY_PAD_COLUMNS
                and (new_row, new_column) not in prev_cells
                and DOOR_KEY_PAD[new_row][new_column] is not None
            ):
                prev_cells_copy = deepcopy(prev_cells)
                prev_cells_copy.add((new_row, new_column))
                directions_copy = deepcopy(directions)
                directions_copy.append((row_change, column_change))
                queue.append([(new_row, new_column), directions_copy, prev_cells_copy])

    if solutions:
        return solutions
    raise ValueError(f"No way to get to target {target} from {pos}")


def get_key_presses_to_directional_key_pad_target_bfs(pos, target):
    queue = deque([(pos, [])])
    visited = set([pos])

    while len(queue) > 0:
        pos, directions = queue.popleft()
        row, column = pos
        if DIRECTIONAL_KEY_PAD[row][column] == target:
            return [direction_to_key_pad_button(direction) for direction in directions]

        for row_change, column_change in DIRECTIONS:
            new_row = row + row_change
            new_column = column + column_change
            if (
                0 <= new_row < DIRECTIONAL_KEY_PAD_ROWS
                and 0 <= new_column < DIRECTIONAL_KEY_PAD_COLUMNS
                and (new_row, new_column) not in visited
                and DIRECTIONAL_KEY_PAD[new_row][new_column] is not None
            ):
                visited.add((new_row, new_column))
                directions_copy = deepcopy(directions)
                directions_copy.append((row_change, column_change))
                queue.append([(new_row, new_column), directions_copy])

    raise ValueError(f"No way to get to target {target} from {pos}")


def get_radiation_robot_key_pad_presses(door_keypad_button):
    global DOOR_ROBOT_POS
    key_presses = get_best_key_preses_to_door_key_pad_target(DOOR_ROBOT_POS, door_keypad_button)
    # Set robot to position it last pressed
    DOOR_ROBOT_POS = door_code_button_to_pos(door_keypad_button)
    # Need to add an activation button press at end so door robot presses button
    return key_presses + ["A"]


def get_cold_robot_key_pad_presses(door_keypad_button):
    global RADIATION_ROBOT_POS
    radiation_robot_key_presses = get_radiation_robot_key_pad_presses(door_keypad_button)
    key_presses = []
    for key_press in radiation_robot_key_presses:
        current_key_presses = get_key_presses_to_directional_key_pad_target_bfs(RADIATION_ROBOT_POS, key_press)
        key_presses += current_key_presses + ["A"]
        RADIATION_ROBOT_POS = directional_button_to_pos(key_press)
    return key_presses


def get_my_key_pad_presses(door_code):
    global COLD_ROBOT_POS
    my_key_presses = []
    for button in door_code:
        cold_robot_key_presses = get_cold_robot_key_pad_presses(button)
        for key_press in cold_robot_key_presses:
            current_key_presses = get_key_presses_to_directional_key_pad_target_bfs(COLD_ROBOT_POS, key_press)
            COLD_ROBOT_POS = directional_button_to_pos(key_press)
            my_key_presses += current_key_presses + ["A"]

    return my_key_presses


# def print_door_keypad(robot_pos):
#     with open("temp.txt", "a") as fp:
#         fp.write("Door Keypad:\n")
#         for row in range(DOOR_KEY_PAD_ROWS):
#             for col in range(DOOR_KEY_PAD_COLUMNS):
#                 if (row, col) == robot_pos:
#                     fp.write("D ")
#                 elif DOOR_KEY_PAD[row][col] is None:
#                     fp.write(" ")
#                 else:
#                     fp.write(DOOR_KEY_PAD[row][col])
#             fp.write("\n")
#         fp.write("\n")


# def print_radiation_control_board(robot_pos):
#     with open("temp.txt", "a") as fp:
#         fp.write("Radiation Control Board:\n")
#         for row in range(DIRECTIONAL_KEY_PAD_ROWS):
#             for col in range(DIRECTIONAL_KEY_PAD_COLUMNS):
#                 if (row, col) == robot_pos:
#                     fp.write("R ")
#                 elif DIRECTIONAL_KEY_PAD[row][col] is None:
#                     fp.write(" ")
#                 else:
#                     fp.write(DIRECTIONAL_KEY_PAD[row][col])
#             fp.write("\n")
#         fp.write("\n")


# def print_cold_control_board(robot_pos):
#     with open("temp.txt", "a") as fp:
#         fp.write("Cold Control Board:\n")
#         for row in range(DIRECTIONAL_KEY_PAD_ROWS):
#             for col in range(DIRECTIONAL_KEY_PAD_COLUMNS):
#                 if (row, col) == robot_pos:
#                     fp.write("C ")
#                 elif DIRECTIONAL_KEY_PAD[row][col] is None:
#                     fp.write(" ")
#                 else:
#                     fp.write(DIRECTIONAL_KEY_PAD[row][col])
#             fp.write("\n")
#         fp.write("\n")


# def print_keypads(door_robot_pos, radiation_robot_pos, cold_robot_pos):
#     with open("temp.txt", "a") as fp:
#         fp.write("-" * 30)
#         fp.write("\n")
#         print_door_keypad(door_robot_pos)
#         print_radiation_control_board(radiation_robot_pos)
#         print_cold_control_board(cold_robot_pos)
#         fp.write("-" * 30)
#         fp.write("\n")


DOOR_KEY_PAD_ACTIVATE_POS = get_door_key_pad_activate_pos()
DIRECTIONAL_KEY_PAD_ACTIVATE_POS = get_directional_key_pad_activate_pos()

complexity = 0
with open("inputs/day21-data.txt", "r") as fp:
    for line in fp:
        DOOR_ROBOT_POS = DOOR_KEY_PAD_ACTIVATE_POS
        RADIATION_ROBOT_POS = DIRECTIONAL_KEY_PAD_ACTIVATE_POS
        COLD_ROBOT_POS = DIRECTIONAL_KEY_PAD_ACTIVATE_POS
        my_key_presses = get_my_key_pad_presses(list(line.strip()))
        print("".join(my_key_presses))
        print(len(my_key_presses))
        complexity += (len(my_key_presses)) * int(line.strip()[:-1])

print(complexity)
