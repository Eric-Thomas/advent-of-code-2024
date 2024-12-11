import math
import time

start_time = time.time()

with open("inputs/day11-data.txt", "r") as fp:
    stones = [int(stone) for stone in list(fp.readline().strip().split())]


cache = {}


def get_stones_after_blinks(stone, blinks):
    if (stone, blinks) in cache:
        return cache[(stone, blinks)]

    if blinks == 0:
        return 1

    stones_total = 0
    if stone == 0:
        stones_total = get_stones_after_blinks(1, blinks - 1)
        cache[(stone, blinks)] = stones_total
        return stones_total
    elif (math.floor(math.log10(stone)) + 1) % 2 == 0:
        stone = str(stone)
        first_stone = int(stone[: len(stone) // 2])
        second_stone = int(stone[len(stone) // 2 :])
        first_stone_total = get_stones_after_blinks(first_stone, blinks - 1)
        cache[(first_stone, blinks - 1)] = first_stone_total
        second_stone_total = get_stones_after_blinks(second_stone, blinks - 1)
        cache[(second_stone, blinks - 1)] = second_stone_total
        stones_total = first_stone_total + second_stone_total
        cache[(stone, blinks)] = stones_total
        return stones_total
    else:
        stones_total = get_stones_after_blinks(stone * 2024, blinks - 1)
        cache[(stone, blinks)] = stones_total
        return stones_total


result = 0
for stone in stones:
    result += get_stones_after_blinks(stone, 75)

print(f"result {result}")
print(f"time elapsed time {time.time() - start_time}")
