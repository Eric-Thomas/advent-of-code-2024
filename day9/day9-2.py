disk_map = []
with open("inputs/day9-data.txt", "r") as fp:
    for line in fp:
        disk_map += [int(num) for num in line.strip()]

drive_size = sum(disk_map)

file_id = 0
filesystem = []
for i in range(0, len(disk_map), 2):
    file = [file_id] * disk_map[i]
    if i + 1 < len(disk_map):
        file += ["."] * disk_map[i + 1]
    filesystem += file
    file_id += 1


def find_next_free_block_on_or_after(filesystem, i):
    if i >= len(filesystem):
        return -1
    start = i
    while start < len(filesystem):
        if filesystem[start] == ".":
            break
        start += 1

    if start < len(filesystem) and filesystem[start] == ".":
        return start

    return -1


def find_next_free_block_start_as_long_as(filesystem, n):
    start = find_next_free_block_on_or_after(filesystem, 0)
    while True:
        end = start
        while end + 1 < len(filesystem) and filesystem[end + 1] == ".":
            end += 1

        if end - start + 1 >= n:
            return start

        start = find_next_free_block_on_or_after(filesystem, end + 1)
        if start == -1:
            return -1


file_block_end = len(filesystem) - 1
while file_block_end > 0:
    file_block_start = file_block_end
    while (
        file_block_start - 1 >= 0
        and filesystem[file_block_start - 1] == filesystem[file_block_end]
    ):
        file_block_start -= 1

    file_block_length = file_block_end - file_block_start + 1

    free_block_start = find_next_free_block_start_as_long_as(
        filesystem, file_block_length
    )
    if 0 <= free_block_start < file_block_start:
        for i in range(file_block_length):
            filesystem[free_block_start + i] = filesystem[file_block_end]
        for i in range(file_block_length):
            filesystem[file_block_start + i] = "."

    file_block_end = file_block_start - 1
    while file_block_end >= 0 and filesystem[file_block_end] == ".":
        file_block_end -= 1


checksum = 0
for i in range(len(filesystem)):
    if filesystem[i] == ".":
        continue
    checksum += i * filesystem[i]

print(f"checksum {checksum}")
