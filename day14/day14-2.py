import re

COLUMNS = 101
ROWS = 103

pattern = re.compile(r"p=(\d{1,3}),(\d{1,3})|v=(-?\d{1,3}),(-?\d{1,3})")
positions_and_velocities = []
with open("inputs/day14-data.txt", "r") as fp:
    for line in fp:
        matches = re.findall(pattern, line)
        position = [int(matches[0][0]), int(matches[0][1])]
        velocity = [int(matches[1][2]), int(matches[1][3])]
        positions_and_velocities.append((position, velocity))


def get_blank_grid():
    grid = []
    for row in range(ROWS):
        current_row = []
        for columns in range(COLUMNS):
            current_row.append(" ")
        grid.append(current_row)
    return grid


def get_positions_after_seconds(seconds, positions_and_velocities):
    index = 0
    positions_after_seconds = [[0, 0] for _ in range(len(positions_and_velocities))]
    for position, velocity in positions_and_velocities:
        pos_x, pos_y = position
        velocity_x, velocity_y = velocity
        pos_x = (pos_x + (seconds * velocity_x)) % COLUMNS
        pos_y = (pos_y + (seconds * velocity_y)) % ROWS
        positions_after_seconds[index][0] = pos_x
        positions_after_seconds[index][1] = pos_y
        index += 1

    return positions_after_seconds


def get_variance_of_positions(positions):
    positions_sum_x = sum([x for x, y in positions])
    positions_sum_y = sum([y for x, y in positions])
    positions_avg_x = positions_sum_x // len(positions)
    positions_avg_y = positions_sum_y // len(positions)
    variance = 0
    for x, y in positions:
        variance += ((x - positions_avg_x) ** 2) + ((y - positions_avg_y) ** 2) // (len(positions) - 1)

    return variance


def write_grid(positions, seconds):
    positions_set = set([(x, y) for x, y in positions])
    grid = get_blank_grid()
    for row in range(ROWS):
        for column in range(COLUMNS):
            if (row, column) in positions_set:
                grid[row][column] = "*"

    with open(f"positions-{seconds}.txt", "w") as fp:
        for line in grid:
            fp.write("".join(line))
            fp.write("\n")


variances_seconds_and_positions = []
for seconds in range(1, ROWS * COLUMNS):
    current_positions = get_positions_after_seconds(seconds, positions_and_velocities)
    variances_seconds_and_positions.append((get_variance_of_positions(current_positions), seconds, current_positions))

variances_seconds_and_positions.sort()

for i in range(10):
    write_grid(variances_seconds_and_positions[i][2], variances_seconds_and_positions[i][1])
