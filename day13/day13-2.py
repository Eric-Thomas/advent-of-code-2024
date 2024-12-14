import re
from typing import Dict, List, Tuple

import numpy as np

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
            x = int(re.findall(prize_x_pattern, line.strip())[0]) + 10000000000000
            y = int(re.findall(prize_y_pattern, line.strip())[0]) + 10000000000000
            current_machine["Prize"] = (x, y)
            claw_machines.append(current_machine)
            current_machine = {}
            parse_line = "separator"
        elif parse_line == "separator":
            parse_line = "A button"


answer = 0
for machine in claw_machines:
    column_vector = np.array(
        [[machine["A button"][0], machine["B button"][0]], [machine["A button"][1], machine["B button"][1]]]
    )

    column_vector_inv = np.linalg.inv(column_vector)

    prize_vector = np.array([[machine["Prize"][0]], [machine["Prize"][1]]])

    solution = np.round(column_vector_inv @ prize_vector, decimals=1)
    a_presses = int(solution[0][0])
    b_presses = int(solution[1][0])
    if (
        a_presses * machine["A button"][0] + b_presses * machine["B button"][0] == machine["Prize"][0]
        and a_presses * machine["A button"][1] + b_presses * machine["B button"][1] == machine["Prize"][1]
    ):
        answer += 3 * a_presses + b_presses


print(answer)
