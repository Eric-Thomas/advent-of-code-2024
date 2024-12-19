from typing import List

patterns = []
designs = []
parsing_patters = True
with open("inputs/day19-data.txt", "r") as fp:
    for line in fp:
        if line.strip() == "":
            parsing_patters = False
            continue

        if parsing_patters:
            patterns += line.strip().split(", ")
        else:
            designs.append(line.strip())

cache = {}


def number_of_valid_designs(design: str, patterns: List[str]):
    if len(design) == 0:
        return 1

    if design in cache:
        return cache[design]

    valid_designs = 0
    for pattern in patterns:
        if design.startswith(pattern):
            valid_designs += number_of_valid_designs(design[len(pattern) :], patterns)

    cache[design] = valid_designs
    return valid_designs


valid_designs = 0
for design in designs:
    valid_designs += number_of_valid_designs(design, patterns)


print(valid_designs)
