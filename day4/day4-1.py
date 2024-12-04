SEARCH_WORD = "XMAS"
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

grid = []
with open("inputs/day4-data.txt") as fp:
    for line in fp:
        grid.append(list(line.strip()))


ROWS = len(grid)
COLUMNS = len(grid[0])


def in_bounds(row, column):
    return 0 <= row < ROWS and 0 <= column < COLUMNS


def dfs(pos, grid):
    row, column = pos
    matches = 0
    for row_change, column_change in DIRECTIONS:
        word_found = True
        current_row = row
        current_column = column
        for search_index in range(1, len(SEARCH_WORD)):
            new_row = current_row + row_change
            new_column = current_column + column_change
            if not in_bounds(new_row, new_column):
                word_found = False
                break
            elif grid[new_row][new_column] != SEARCH_WORD[search_index]:
                word_found = False
                break
            else:
                current_row = new_row
                current_column = new_column
        if word_found:
            matches += 1

    return matches


matches = 0
for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column] == "X":
            matches += dfs((row, column), grid)


print(matches)
