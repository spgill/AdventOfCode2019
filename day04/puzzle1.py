# stdlib imports
import re

# vendor imports
import click


def isValidCode(n):
    lastDigit = 0

    # Check against decreasing digit value
    for digit in str(n):
        if int(digit) < int(lastDigit):
            return False
        lastDigit = digit

    # Check for the presence of at least one repeating digit pair
    if not len(re.findall(r"((\d)\2+)", str(n))):
        return False

    return True


@click.command()
@click.argument("input_range", type=str)
def main(input_range):
    """Put your puzzle execution code here"""
    # Deserialize the start and stop of the input range
    rangeStart, rangeStop = [int(s) for s in input_range.split("-")]

    # Map the range to the validity checking function and sum the True's
    print("RESULT:", sum(map(isValidCode, range(rangeStart, rangeStop + 1))))


# Execute cli function on main
if __name__ == "__main__":
    main()
