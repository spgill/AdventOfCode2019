# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Convert the comma-delimited string of numbers into a list of ints
    register = list(
        map(lambda op: int(op), input_file.read().strip().split(","))
    )

    # Modify the second and third codes for the final result
    register[1] = 12
    register[2] = 2

    # We will start reading the opcodes at position 0
    pointer = 0

    # Loop infinitely until we reach the termination instruction
    while True:
        # Get the code at the current read position
        code = register[pointer]

        # Code 99 means immediate termination
        if code == 99:
            break

        # Code 1 is addition
        elif code == 1:
            # Get register addresses
            addendAPointer = register[pointer + 1]
            addendBPointer = register[pointer + 2]
            sumPointer = register[pointer + 3]

            # Perform the addition
            register[sumPointer] = (
                register[addendAPointer] + register[addendBPointer]
            )

            # Advance the code position by 4
            pointer += 4

        # Code 2 is multiplication
        elif code == 2:
            # Get register addresses
            factorAPointer = register[pointer + 1]
            factorBPointer = register[pointer + 2]
            productPointer = register[pointer + 3]

            # Perform the addition
            register[productPointer] = (
                register[factorAPointer] * register[factorBPointer]
            )

            # Advance the code position by 4
            pointer += 4

        # Unknown opcode means there was an error
        else:
            raise RuntimeError(f"Unknown opcode {code} at position {pointer}")

    # Print the the result remaining in postion 0
    print("RESULT:", register[0])


# Execute cli function on main
if __name__ == "__main__":
    main()
