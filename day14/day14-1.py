import re
from collections import defaultdict

COLUMNS = 101
ROWS = 103
SECONDS = 100

pattern = re.compile(r"p=(\d{1,3}),(\d{1,3})|v=(-?\d{1,3}),(-?\d{1,3})")
positions_and_velocities = []
with open("inputs/day14-data.txt", "r") as fp:
    for line in fp:
        matches = re.findall(pattern, line)
        position = [int(matches[0][0]), int(matches[0][1])]
        velocity = [int(matches[1][2]), int(matches[1][3])]
        positions_and_velocities.append((position, velocity))

index = 0
for position, velocity in positions_and_velocities:
    pos_x, pos_y = position
    velocity_x, velocity_y = velocity
    pos_x = (pos_x + (SECONDS * velocity_x)) % COLUMNS
    pos_y = (pos_y + (SECONDS * velocity_y)) % ROWS
    positions_and_velocities[index][0][0] = pos_x
    positions_and_velocities[index][0][1] = pos_y
    index += 1

quadrants = defaultdict(int)
for i in range(len(positions_and_velocities)):
    if positions_and_velocities[i][0][0] < COLUMNS // 2:
        if positions_and_velocities[i][0][1] < ROWS // 2:
            quadrants["top left"] += 1
        elif positions_and_velocities[i][0][1] > ROWS // 2:
            quadrants["bottom left"] += 1
    elif positions_and_velocities[i][0][0] > COLUMNS // 2:
        if positions_and_velocities[i][0][1] < ROWS // 2:
            quadrants["top right"] += 1
        elif positions_and_velocities[i][0][1] > ROWS // 2:
            quadrants["bottm right"] += 1

answer = 1
for robots in quadrants.values():
    answer *= robots

print(answer)
