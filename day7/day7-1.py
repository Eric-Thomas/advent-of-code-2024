equations = {}
with open("inputs/day7-data.txt", "r") as fp:
    for line in fp:
        test_value, operands = line.strip().split(":")
        equations[int(test_value)] = list(map(int, operands.strip().split()))

OPERATORS = ["+", "*"]


def dfs(i, test_value, operands, result):
    """Backtracking algorithm that will test each operator in each position until result
    equals the test_value or we run out of operands.
    i must start at 1 because we are applying the operator to the operands
    at that index index and result must start at operands[0].
    This is because we are applying the operator at pos i in operands to result.
    Ex: operands = [7, 3, 5] and i = 1 and result = 7. We apply + or * to result and operands[i]
    so 7 * 3 and 7 + 3"""

    # Need to check that values are equal and we've used all operands
    if result == test_value and i == len(operands):
        return True

    # Total number of operators should be number of operands -1
    # Ex: 2 operands will have 1 operator
    # 3 operands will have 2 operators
    if i >= len(operands):
        return False

    for operator in OPERATORS:
        # apply operator to current value
        if operator == "+":
            result += operands[i]
            if dfs(i + 1, test_value, operands, result):
                return True
        elif operator == "*":
            result *= operands[i]
            if dfs(i + 1, test_value, operands, result):
                return True

        # invert operator from result to backtrack
        if operator == "+":
            result -= operands[i]
        elif operator == "*":
            result /= operands[i]

    return False


total_calibration_result = 0
for test_value, operands in equations.items():
    if dfs(1, test_value, operands, operands[0]):
        total_calibration_result += test_value


print(f"total calibration result {total_calibration_result}")
