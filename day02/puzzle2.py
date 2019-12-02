# stdlib imports
import copy

# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Convert the comma-delimited string of numbers into a list of ints
    masterRegister = list(
        map(lambda op: int(op), input_file.read().strip().split(","))
    )

    def execute(noun, verb):
        # Create a local copy of the register for this execution
        register = copy.deepcopy(masterRegister)

        # Inject the noun and verb
        register[1] = noun
        register[2] = verb

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
                raise RuntimeError(
                    f"Unknown opcode {code} at position {pointer}"
                )

        # Return the result
        return register[0]

    # Iterate through all the possible combinations until the target is found
    target = 19690720
    found = None
    for noun in range(100):
        for verb in range(100):
            result = execute(noun, verb)
            if result == target:
                found = (noun, verb)
                break
        if found:
            break

    # Calculate the final result
    print("RESULT:", 100 * found[0] + found[1])


# Execute cli function on main
if __name__ == "__main__":
    main()
