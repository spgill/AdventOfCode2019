# stdlib imports
import enum
import itertools

# vendor imports
import click


class IntCodeMachineState(enum.Enum):
    CLEAN = enum.auto()
    HALTED = enum.auto()
    WAITING_FOR_INPUT = enum.auto()


class IntCodeMachine:
    def __init__(self, instructions):
        # Machine starts in a clean state
        self.state = IntCodeMachineState.CLEAN

        # Convert the comma-delimited string of numbers into a list of ints
        self.memory = list(
            map(lambda op: int(op), instructions.strip().split(","))
        )

        # Input value is None
        self.inputValue = None

        # Empty list to capture output values
        self.outputValues = []

        # We will start reading the opcodes at position 0
        self.position = 0

    # Recursive function to split a decimal into digits
    def getDigits(self, n):
        if n < 10:
            return [n]
        else:
            r = self.getDigits(n // 10)
            return r + [n % 10]

    def splitInstruction(self, n):
        # Split the instruction into digits and reverse them
        digits = list(reversed(self.getDigits(n)))

        # Zero fill the digits array
        for i in range(5 - len(digits)):
            digits.append(0)

        # Consolidate the ones and tens place into an opcode
        opcode = digits[0] + 10 * digits[1]

        # Return the opcode and param modes
        return (opcode, digits[2], digits[3], digits[4])

    def resolveValue(self, memory, param, paramMode):
        # If in immediate mode, return the value directly
        if paramMode == 1:
            return param

        # Else, treat it as a pointer
        else:
            return memory[param]

    def execute(self):
        # Make surethe machine isn't already halted
        if self.state is IntCodeMachineState.HALTED:
            raise RuntimeError("Machine is already halted")

        # Loop infinitely until we reach the termination instruction
        while True:
            # Get the code at the current read position
            instruction = self.memory[self.position]

            # Split the opcode and params apart
            opcode, paramModeA, paramModeB, paramModeC = self.splitInstruction(
                instruction
            )

            # Code 99 means immediate termination
            if opcode == 99:
                self.state = IntCodeMachineState.HALTED
                break

            # Code 1 is addition
            elif opcode == 1:
                # Get memory values
                paramA = self.resolveValue(
                    self.memory, self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory, self.memory[self.position + 2], paramModeB
                )
                sumPointer = self.memory[self.position + 3]

                # print("ADD", paramA, paramB, "->", sumPointer)

                # Perform the addition
                self.memory[sumPointer] = paramA + paramB

                # Advance the code position by 4
                self.position += 4

            # Code 2 is multiplication
            elif opcode == 2:
                # Get memory values
                paramA = self.resolveValue(
                    self.memory, self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory, self.memory[self.position + 2], paramModeB
                )
                productPointer = self.memory[self.position + 3]

                # Perform the addition
                self.memory[productPointer] = paramA * paramB

                # Advance the code position by 4
                self.position += 4

            # Code 3 is input
            elif opcode == 3:
                # If input is not available, stop execution
                if self.inputValue is None:
                    self.state = IntCodeMachineState.WAITING_FOR_INPUT
                    break

                # Store the value at the indicated pointer position
                outPointer = self.memory[self.position + 1]
                self.memory[outPointer] = self.inputValue

                # Zero out the input value
                self.inputValue = None

                # Advance the code position
                self.position += 2

            # Code 4 is output
            elif opcode == 4:
                # Determine the value and print it
                value = self.resolveValue(
                    self.memory, self.memory[self.position + 1], paramModeA
                )
                self.outputValues.append(value)

                # Advance the code position
                self.position += 2

            # Code 5 and 6 are conditional jumps
            elif opcode in [5, 6]:
                # Get memory values
                paramA = self.resolveValue(
                    self.memory, self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory, self.memory[self.position + 2], paramModeB
                )

                # If non-zero, set the position pointer
                if (opcode == 5 and paramA != 0) or (
                    opcode == 6 and paramA == 0
                ):
                    self.position = paramB

                # Else, do nothing and advance the position naturally
                else:
                    self.position += 3

            # Code 7 and 8 are comparison
            elif opcode in [7, 8]:
                # Get memory values
                paramA = self.resolveValue(
                    self.memory, self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory, self.memory[self.position + 2], paramModeB
                )
                outputPointer = self.memory[self.position + 3]

                # Determine the value based on the opcode
                if opcode == 7:
                    flag = paramA < paramB
                elif opcode == 8:
                    flag = paramA == paramB

                # Write the value to memory
                self.memory[outputPointer] = int(flag)

                # Advance the code position by 4
                self.position += 4

            # Unknown opcode means there was an error
            else:
                raise RuntimeError(
                    f"Unknown opcode {opcode} ({instruction}) at position {self.position}"
                )


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Load the amplifier software instructions
    amplifierSoftware = input_file.read().strip()

    # List to catch all output signals
    outputSignals = []

    # Iterate through all permutations of phase signals
    for permutation in itertools.permutations(range(5, 10)):
        amplifiers = []

        # Use the phase value to create an intcode machine
        for phase in permutation:
            machine = IntCodeMachine(amplifierSoftware)

            # First execution is for the phase setting
            machine.inputValue = phase
            machine.execute()

            amplifiers.append(machine)

        # Loop through each machine in order until execution halts on the last
        previousValue = 0
        while True:
            for i, machine in enumerate(amplifiers):
                machine.inputValue = previousValue
                machine.execute()
                previousValue = machine.outputValues.pop(0)

                # When the last amp halts, that's the end
                if i == 4 and machine.state is IntCodeMachineState.HALTED:
                    break
            else:
                continue
            break

        outputSignals.append(previousValue)

    # Result is the highest output signal
    print("RESULT:", max(outputSignals))


# Execute cli function on main
if __name__ == "__main__":
    main()
