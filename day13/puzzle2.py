# stdlib imports
import enum
import math
import sys
import time

# vendor imports
import click

# local imports
from common.intcode import IntCodeMachine, IntCodeMachineState
from common.iteration import every


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
