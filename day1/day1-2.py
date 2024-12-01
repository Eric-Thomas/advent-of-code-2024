from collections import defaultdict

with open("inputs/day1-data.txt", "r") as fp:
    count = defaultdict(int)
    left = []
    for line in fp:
        left_val, right_val = line.split()
        left.append(left_val)
        count[right_val] += 1

similarity = 0
for val in left:
    similarity += int(val) * count[val]

print(f"Similarity score - {similarity}")
