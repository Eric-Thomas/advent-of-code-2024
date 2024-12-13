import re
from collections import defaultdict
from typing import Dict, List, Tuple

claw_machines: List[Dict[str, Tuple[str, str]]] = []
parse_line = "A button"
current_machine = {}
button_x_pattern = re.compile(r"X\+(\d+)")
button_y_pattern = re.compile(r"Y\+(\d+)")
prize_x_pattern = re.compile(r"X=(\d+)")
prize_y_pattern = re.compile(r"Y=(\d+)")
with open("inputs/day13-data.txt", "r") as fp:
    for line in fp:
        if parse_line == "A button":
            x = int(re.findall(button_x_pattern, line.strip())[0])
            y = int(re.findall(button_y_pattern, line.strip())[0])
            current_machine["A button"] = (x, y)
            parse_line = "B button"
        elif parse_line == "B button":
            x = int(re.findall(button_x_pattern, line.strip())[0])
            y = int(re.findall(button_y_pattern, line.strip())[0])
            current_machine["B button"] = (x, y)
            parse_line = "Prize"
        elif parse_line == "Prize":
            x = int(re.findall(prize_x_pattern, line.strip())[0])
            y = int(re.findall(prize_y_pattern, line.strip())[0])
            current_machine["Prize"] = (x, y)
            claw_machines.append(current_machine)
            current_machine = {}
            parse_line = "separator"
        elif parse_line == "separator":
            parse_line = "A button"


answer = 0
for machine in claw_machines:
    solutions = []
    for a_presses in range(100):
        x = a_presses * machine["A button"][0]
        y = a_presses * machine["A button"][1]
        x_remaining = machine["Prize"][0] - x
        y_remaining = machine["Prize"][1] - y

        if (
            x_remaining % machine["B button"][0] == 0
            and y_remaining % machine["B button"][1] == 0
            and x_remaining // machine["B button"][0] == y_remaining // machine["B button"][1]
        ):
            b_presses = x_remaining // machine["B button"][0]
            solutions.append((a_presses, b_presses))

    if solutions:
        answer += min([3 * a_presses + b_presses for a_presses, b_presses in solutions])


print(answer)
