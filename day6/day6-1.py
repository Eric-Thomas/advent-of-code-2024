from typing import List

grid: List[List[str]] = []
guard_pos = None
with open("inputs/day6-data.txt") as fp:
    for row, line in enumerate(fp):
        line = line.strip()
        grid.append([])
        for column, char in enumerate(line):
            if char == "^":
                guard_pos = (row, column)
                # Replace guard with "." so we don't have to keep track of ^ character
                char = "."
            grid[row].append(char)


def get_next_pos(pos, direction):
    row, column = pos

    if direction == "up":
        return (row - 1, column)
    elif direction == "down":
        return (row + 1, column)
    elif direction == "left":
        return (row, column - 1)
    elif direction == "right":
        return (row, column + 1)

    raise ValueError(f"direction must be in ['up', 'down', 'left', 'right']")


def rotate(direction):
    if direction == "up":
        return "right"
    elif direction == "right":
        return "down"
    elif direction == "down":
        return "left"
    elif direction == "left":
        return "up"
    raise ValueError(f"direction must be in ['up', 'down', 'left', 'right']")


positions_visited = set([guard_pos])
direction = "up"
while True:
    next_pos = get_next_pos(guard_pos, direction)
    row, column = next_pos
    if row < 0 or row >= len(grid) or column < 0 or column >= len(grid[0]):
        print("Guard left the room")
        print(f"Positions visited {len(positions_visited)}")
        break
    if grid[row][column] == "#":
        direction = rotate(direction)
    elif grid[row][column] == ".":
        positions_visited.add(next_pos)
        guard_pos = next_pos
