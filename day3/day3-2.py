import re

pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")

with open("inputs/day3-data.txt", "r", encoding="utf-8") as fp:
    memory = fp.read()


operations = re.findall(pattern, memory)

mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
total = 0
mul_enabled = True
for operation in operations:
    if operation == "do()":
        mul_enabled = True
    elif operation == "don't()":
        mul_enabled = False
    else:
        match = mul_pattern.match(operation)
        if mul_enabled:
            left_operand, right_operand = match.groups()
            total += int(left_operand) * int(right_operand)


print(total)
