REGISTER_A = 0  # Don't include input bc of Eric's ask
REGISTER_B = 0
REGISTER_C = 0

PROGRAM = []  # Don't include input bc of Eric's ask
INSTRUCTION_POINTER = 0


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


output = []
while INSTRUCTION_POINTER < len(PROGRAM):
    opcode, operand = PROGRAM[INSTRUCTION_POINTER : INSTRUCTION_POINTER + 2]
    operation_output, INSTRUCTION_POINTER = get_operation_output_and_next_instruction_pos(
        opcode, operand, INSTRUCTION_POINTER
    )
    if operation_output is not None:
        output.append(operation_output)


print(",".join([str(x) for x in output]))
