import re

pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

with open("inputs/day3-data.txt", "r", encoding="utf-8") as fp:
    memory = fp.read()


operations = re.findall(pattern, memory)


total = 0

for left_operand, right_operand in operations:
    total += int(left_operand) * int(right_operand)

print(total)
