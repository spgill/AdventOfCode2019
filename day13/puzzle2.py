# stdlib imports
import array
import enum
import math
import sys
import time

# vendor imports
import click


def every(iterable, n):
    assert len(iterable) % n == 0
    stack = list()
    for i in iterable:
        stack.append(i)
        if len(stack) == n:
            yield tuple(stack)
            stack = list()


class IntCodeMachineState(enum.Enum):
    CLEAN = enum.auto()
    HALTED = enum.auto()
    WAITING_FOR_INPUT = enum.auto()


class IntCodeMachine:
    def __init__(self, instructions):
        # Machine starts in a clean state
        self.state = IntCodeMachineState.CLEAN

        # Convert the comma-delimited string of numbers into a memory-
        # efficient array of signed long long's
        self.memory = array.array(
            "q", map(lambda op: int(op), instructions.strip().split(","))
        )

        # Input value is None
        self.inputValue = None

        # Empty list to capture output values
        self.outputValues = []

        # Starting register values
        self.position = 0
        self.relativeBase = 0

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

    def resolveValue(self, param, paramMode):
        # If in immediate mode, return the value directly
        if paramMode == 1:
            return param

        # If in relative mode, modify the pointer relative to the base
        elif paramMode == 2:
            param += self.relativeBase

        # If the address is larger than the memory space, return 0
        if param >= len(self.memory):
            return 0
        return self.memory[param]

    def assignValue(self, address, mode, value):
        # If relative mode is specified, make the address relative to the base
        if mode == 2:
            address += self.relativeBase

        # If trying to assign to an address outside of memory space,
        # allocate more memory space
        if address >= len(self.memory):
            for i in range(address - len(self.memory) + 1):
                self.memory.append(0)

        # Assign the value
        self.memory[address] = value

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

            # Code 1 and 2 are arithmatic
            elif opcode in [1, 2]:
                # Get memory values
                paramA = self.resolveValue(
                    self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory[self.position + 2], paramModeB
                )

                # Perform the addition
                self.assignValue(
                    self.memory[self.position + 3],
                    paramModeC,
                    paramA + paramB if opcode == 1 else paramA * paramB,
                )

                # Advance the code position by 4
                self.position += 4

            # Code 3 is input
            elif opcode == 3:
                # If input is not available, stop execution
                if self.inputValue is None:
                    self.state = IntCodeMachineState.WAITING_FOR_INPUT
                    break

                # Store the value at the indicated pointer position
                self.assignValue(
                    self.memory[self.position + 1], paramModeA, self.inputValue
                )

                # Zero out the input value
                self.inputValue = None

                # Advance the code position
                self.position += 2

            # Code 4 is output
            elif opcode == 4:
                # Determine the value and print it
                value = self.resolveValue(
                    self.memory[self.position + 1], paramModeA
                )
                self.outputValues.append(value)

                # Advance the code position
                self.position += 2

            # Code 5 and 6 are conditional jumps
            elif opcode in [5, 6]:
                # Get memory values
                paramA = self.resolveValue(
                    self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory[self.position + 2], paramModeB
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
                    self.memory[self.position + 1], paramModeA
                )
                paramB = self.resolveValue(
                    self.memory[self.position + 2], paramModeB
                )

                # Determine the value based on the opcode
                if opcode == 7:
                    flag = paramA < paramB
                elif opcode == 8:
                    flag = paramA == paramB

                # Write the value to memory
                self.assignValue(
                    self.memory[self.position + 3], paramModeC, int(flag)
                )

                # Advance the code position by 4
                self.position += 4

            # Code 9 adjust the relative base
            elif opcode == 9:
                # Determine the value and modify the base
                self.relativeBase += self.resolveValue(
                    self.memory[self.position + 1], paramModeA
                )

                # Advance the code position
                self.position += 2

            # Unknown opcode means there was an error
            else:
                raise RuntimeError(
                    f"Unknown opcode {opcode} ({instruction}) at position {self.position}"
                )


class TileType(enum.Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


tileCharacters = {
    TileType.EMPTY: " ",
    TileType.WALL: "█",
    TileType.BLOCK: "░",
    TileType.PADDLE: "─",
    TileType.BALL: "o",
}


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.option("--user-control", "-u", is_flag=True)
@click.option("--visualize", "-v", is_flag=True)
def main(input_file, user_control, visualize):
    print("WARNING: This may take a while")

    # Load program from input file
    arcadeProgram = input_file.read().strip()

    # Create a new intcode machine, add quarters, and execute
    machine = IntCodeMachine(arcadeProgram)
    machine.memory[0] = 2  # 2 quarters

    # Loop until all blocks are broken
    blocks = math.inf
    while blocks > 0:
        # Execute machine until next interrupt
        machine.execute()

        # Iterate through output values to construct tiles and read score
        board = dict()
        xMax = 0
        yMax = 0
        score = 0
        ballX = 0
        paddleX = 0
        for x, y, tileId in every(machine.outputValues, 3):
            # x -1 and y 0 are the signals for the score output
            if x == -1 and y == 0:
                score = tileId
                continue

            tile = TileType(tileId)

            # Track ball and paddle position
            if tile is TileType.BALL:
                ballX = x
            elif tile is TileType.PADDLE:
                paddleX = x

            board[(x, y)] = tile
            xMax = max(xMax, x)
            yMax = max(yMax, y)

        # Update block count
        blocks = len(
            list(filter(lambda item: item[1] is TileType.BLOCK, board.items()))
        )

        # Draw the board to the console if visualize flag enabled
        if visualize:
            print("CURRENT SCORE:", score)
            for y in range(yMax + 1):
                for x in range(xMax + 1):
                    sys.stdout.write(tileCharacters[board[(x, y)]])
                sys.stdout.write("\n")
            print()

        # If the game is waiting on input, get the key from console
        if machine.state is IntCodeMachineState.WAITING_FOR_INPUT:
            # If user control is activated, let the user controll the paddle
            if user_control:
                while True:
                    button = click.getchar()
                    if button == "a":
                        button = -1
                        break
                    elif button == "d":
                        button = 1
                        break
                    elif button == " ":
                        button = 0
                        break
                    print("INVALID INPUT!")
                machine.inputValue = button

            # Else, track the ball with the paddle
            else:
                if ballX < paddleX:
                    machine.inputValue = -1
                elif ballX > paddleX:
                    machine.inputValue = 1
                else:
                    machine.inputValue = 0

                # If visualizing, artificially slow down execution
                if visualize:
                    time.sleep(0.001)

        # Handle halt state
        elif machine.state is IntCodeMachineState.HALTED:
            # If there are blocks left, you lose
            if blocks > 0:
                print("YOU LOSE")
                break

            # Else, you win. Print the final score.
            else:
                print("RESULT:", score)
                break

        # Invalid state????
        else:
            raise RuntimeError(f"Invalid machine state: {machine.state}")


# Execute cli function on main
if __name__ == "__main__":
    main()
