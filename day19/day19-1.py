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


def design_valid(design: str, patterns: List[str]):
    if len(design) == 0 or design in patterns:
        return True

    for pattern in patterns:
        if design.startswith(pattern):
            if design_valid(design[len(pattern) :], patterns):
                return True

    return False


valid_designs = 0
for design in designs:
    if design_valid(design, patterns):
        valid_designs += 1

print(valid_designs)
