def get_combo_operand(operand):
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return REGISTER_A
    if operand == 5:
        return REGISTER_B
    if operand == 6:
        return REGISTER_C

    raise ValueError(f"Operand {operand} is not valid (0-6)")


def get_operation_output_and_next_instruction_pos(opcode, operand, instruction_pointer):
    global REGISTER_A
    global REGISTER_B
    global REGISTER_C
    if opcode == 0:
        REGISTER_A = REGISTER_A // (2 ** get_combo_operand(operand))
        return None, instruction_pointer + 2
    elif opcode == 1:
        REGISTER_B = REGISTER_B ^ operand
        return None, instruction_pointer + 2
    elif opcode == 2:
        REGISTER_B = get_combo_operand(operand) % 8
        return None, instruction_pointer + 2
    elif opcode == 3:
        if REGISTER_A != 0:
            return None, operand
        return None, instruction_pointer + 2
    elif opcode == 4:
        REGISTER_B = REGISTER_B ^ REGISTER_C
        return None, instruction_pointer + 2
    elif opcode == 5:
        return get_combo_operand(operand) % 8, instruction_pointer + 2
    elif opcode == 6:
        REGISTER_B = REGISTER_A // (2 ** get_combo_operand(operand))
        return None, instruction_pointer + 2
    elif opcode == 7:
        REGISTER_C = REGISTER_A // (2 ** get_combo_operand(operand))
        return None, instruction_pointer + 2


PROGRAM = []  # Don't include input bc of Eric's ask
output = []
initial_a = 8 ** (len(PROGRAM) - 1)
# Changing by powers of 8 ^ n changes n through n + 2 digits
# So if we change A input by 8 ^ 6 then digits 6, 7, and 8 will change
# Initialize this so we modify the rightmost digit and decrese this 1 when we match it
power_of_8 = len(PROGRAM) - 2
while output != PROGRAM:
    initial_a += 8**power_of_8
    REGISTER_A = initial_a
    REGISTER_B = 0
    REGISTER_C = 0
    INSTRUCTION_POINTER = 0
    output = []
    while INSTRUCTION_POINTER < len(PROGRAM):
        opcode, operand = PROGRAM[INSTRUCTION_POINTER : INSTRUCTION_POINTER + 2]
        operation_output, INSTRUCTION_POINTER = get_operation_output_and_next_instruction_pos(
            opcode, operand, INSTRUCTION_POINTER
        )
        if operation_output is not None:
            output.append(operation_output)
    if output[power_of_8 + 2 :] == PROGRAM[power_of_8 + 2 :]:
        power_of_8 -= 1
        if power_of_8 < 0:
            power_of_8 = 0

print(initial_a)
