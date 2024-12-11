import math
import time

start_time = time.time()

with open("inputs/day11-data.txt", "r") as fp:
    stones = [int(stone) for stone in list(fp.readline().strip().split())]


for _ in range(25):
    i = 0
    while i < len(stones):
        if stones[i] == 0:
            stones[i] = 1
        elif (math.floor(math.log10(stones[i])) + 1) % 2 == 0:
            stone = str(stones[i])
            stones[i] = int(stone[: len(stone) // 2])
            stones.insert(i + 1, int(stone[len(stone) // 2 :]))
            # Move pointer forward 1 so we don't act on this stone until next iteration
            i += 1
        else:
            stones[i] *= 2024

        i += 1

print(len(stones))
print(f"time elapsed time {time.time() - start_time}")
