from collections import defaultdict

grid = []
with open("inputs/day8-data.txt", "r") as fp:
    for line in fp:
        grid.append(list(line.strip()))


ROWS = len(grid)
COLS = len(grid[0])

antenna_to_pos = defaultdict(list)
for row in range(ROWS):
    for column in range(COLS):
        if grid[row][column] != ".":
            antenna_to_pos[grid[row][column]].append((row, column))


antinodes = set()
for antenna, positions in antenna_to_pos.items():
    for i in range(len(positions)):
        for j in range(len(positions)):
            if i == j:
                continue
            p1_row, p1_column = positions[i]
            # Add antinodes at each antenna pos if there are more than 1 antennas
            antinodes.add((p1_row, p1_column))
            p2_row, p2_column = positions[j]

            row_diff = p1_row - p2_row
            column_diff = p1_column - p2_column

            antinode_row = p1_row + row_diff
            antinode_column = p1_column + column_diff
            while (
                0 <= antinode_row < ROWS
                and 0 <= antinode_column < COLS
                and grid[antinode_row][antinode_column] != grid[p1_row][p1_column]
            ):
                antinodes.add((antinode_row, antinode_column))
                antinode_row += row_diff
                antinode_column += column_diff

print(f"Antinodes {len(antinodes)}")
