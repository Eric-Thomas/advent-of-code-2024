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


left, right = 0, len(filesystem) - 1

while left < right:
    if left == 26:
        print("breakpoint")
    while left < len(filesystem) and filesystem[left] != ".":
        left += 1

    while right >= 0 and filesystem[right] == ".":
        right -= 1

    if left < right:
        filesystem[left] = filesystem[right]
        filesystem[right] = "."

checksum = 0
for i in range(len(filesystem)):
    if filesystem[i] == ".":
        break
    checksum += i * filesystem[i]

print(f"checksum {checksum}")
