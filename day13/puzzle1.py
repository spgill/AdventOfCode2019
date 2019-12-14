# stdlib imports
import enum

# vendor imports
import click

# local imports
from common.intcode import IntCodeMachine
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
def main(input_file):
    # Load program from input file
    arcadeProgram = input_file.read().strip()

    # Create a new intcode machine and execute
    machine = IntCodeMachine(arcadeProgram)
    machine.execute()

    # The result is just the number of blocks
    print(
        "RESULT:",
        len(list(filter(lambda t: t[2] == 2, every(machine.outputValues, 3)))),
    )


# Execute cli function on main
if __name__ == "__main__":
    main()
