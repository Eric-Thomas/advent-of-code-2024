with open("inputs/day2-data.txt", "r") as fp:
    levels = []
    for line in fp:
        levels.append([int(reading) for reading in line.strip().split()])

safe_count = 0

for level in levels:
    increasing_level = level[1] > level[0]
    safe = True
    for i in range(1, len(level)):
        if increasing_level:
            if not (1 <= level[i] - level[i - 1] <= 3):
                safe = False
                break
        else:
            if not (1 <= level[i - 1] - level[i] <= 3):
                safe = False
                break

    if safe:
        safe_count += 1

print(f"Safe count - {safe_count}")
