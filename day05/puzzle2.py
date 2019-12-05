# vendor imports
import click


# Recursive function to split a decimal into digits
def getDigits(n):
    if n < 10:
        return [n]
    else:
        r = getDigits(n // 10)
        return r + [n % 10]


def splitInstruction(n):
    # Split the instruction into digits and reverse them
    digits = list(reversed(getDigits(n)))

    # Zero fill the digits array
    for i in range(5 - len(digits)):
        digits.append(0)

    # Consolidate the ones and tens place into an opcode
    opcode = digits[0] + 10 * digits[1]

    # Return the opcode and param modes
    return (opcode, digits[2], digits[3], digits[4])


def resolveValue(memory, param, paramMode):
    # If in immediate mode, return the value directly
    if paramMode == 1:
        return param

    # Else, treat it as a pointer
    else:
        return memory[param]


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Convert the comma-delimited string of numbers into a list of ints
    memory = list(
        map(lambda op: int(op), input_file.read().strip().split(","))
    )

    # We will start reading the opcodes at position 0
    position = 0

    # Loop infinitely until we reach the termination instruction
    while True:
        # Get the code at the current read position
        instruction = memory[position]

        # Split the opcode and params apart
        opcode, paramModeA, paramModeB, paramModeC = splitInstruction(
            instruction
        )

        # Code 99 means immediate termination
        if opcode == 99:
            break

        # Code 1 is addition
        elif opcode == 1:
            # Get memory values
            paramA = resolveValue(memory, memory[position + 1], paramModeA)
            paramB = resolveValue(memory, memory[position + 2], paramModeB)
            sumPointer = memory[position + 3]

            # print("ADD", paramA, paramB, "->", sumPointer)

            # Perform the addition
            memory[sumPointer] = paramA + paramB

            # Advance the code position by 4
            position += 4

        # Code 2 is multiplication
        elif opcode == 2:
            # Get memory values
            paramA = resolveValue(memory, memory[position + 1], paramModeA)
            paramB = resolveValue(memory, memory[position + 2], paramModeB)
            productPointer = memory[position + 3]

            # Perform the addition
            memory[productPointer] = paramA * paramB

            # Advance the code position by 4
            position += 4

        # Code 3 is input
        elif opcode == 3:
            # Prompt the user for input
            value = int(input(f"Input at position {position}> "))

            # Store the value at the indicated pointer position
            outPointer = memory[position + 1]
            memory[outPointer] = value

            # Advance the code position
            position += 2

        # Code 4 is output
        elif opcode == 4:
            # Determine the value and print it
            value = resolveValue(memory, memory[position + 1], paramModeA)
            print(f"Output at position {position}: {value}")

            # Advance the code position
            position += 2

        # Code 5 and 6 are conditional jumps
        elif opcode in [5, 6]:
            # Get memory values
            paramA = resolveValue(memory, memory[position + 1], paramModeA)
            paramB = resolveValue(memory, memory[position + 2], paramModeB)

            # If non-zero, set the position pointer
            if (opcode == 5 and paramA != 0) or (opcode == 6 and paramA == 0):
                position = paramB

            # Else, do nothing and advance the position naturally
            else:
                position += 3

        # Code 7 and 8 are comparison
        elif opcode in [7, 8]:
            # Get memory values
            paramA = resolveValue(memory, memory[position + 1], paramModeA)
            paramB = resolveValue(memory, memory[position + 2], paramModeB)
            outputPointer = memory[position + 3]

            # Determine the value based on the opcode
            if opcode == 7:
                flag = paramA < paramB
            elif opcode == 8:
                flag = paramA == paramB

            # Write the value to memory
            memory[outputPointer] = int(flag)

            # Advance the code position by 4
            position += 4

        # Unknown opcode means there was an error
        else:
            raise RuntimeError(
                f"Unknown opcode {opcode} ({instruction}) at position {position}"
            )

    # Print the the result remaining in postion 0
    print("Result is the last output above.")


# Execute cli function on main
if __name__ == "__main__":
    main()
