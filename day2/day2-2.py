from typing import List


def parse_levels():
    with open("inputs/day2-data.txt", "r") as fp:
        levels = []
        for line in fp:
            levels.append([int(reading) for reading in line.strip().split()])

    return levels


def index_of_unsafe_reading(level: List[int], increasing: bool) -> int:
    """Returns the index of the unsafe reading for a level. If not such
    index exists, returns -1
    """

    for i in range(1, len(level)):
        if increasing:
            if not (1 <= level[i] - level[i - 1] <= 3):
                return i
        else:
            if not (1 <= level[i - 1] - level[i] <= 3):
                return i

    return -1


levels = parse_levels()
safe_count = 0
for level in levels:
    increasing_level = level[1] > level[0]
    if index_of_unsafe_reading(level, increasing_level) == -1:
        safe_count += 1
    else:
        # Brute force solution to try removing each element and checking if it's safe
        for i in range(len(level)):
            new_list_current_removed = level[:i] + level[i + 1 :]
            if (
                index_of_unsafe_reading(
                    new_list_current_removed, new_list_current_removed[1] > new_list_current_removed[0]
                )
                == -1
            ):
                safe_count += 1
                break


print(f"Safe count - {safe_count}")
