# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Decode the input into lines
    lineData = input_file.read().strip().splitlines()
    lineCoordinates = []

    # Iterate through each set of line data (only 2)
    for path in lineData:
        coordinates = []

        # Starting point is the origin (0, 0)
        x = 0
        y = 0

        # Iterate through each instruction in the path
        for instruction in path.split(","):
            direction = instruction[0]
            magnitude = int(instruction[1:])

            # Iterate through a range to generate coordinates
            for i in range(magnitude):
                if direction == "U":
                    y += 1
                elif direction == "R":
                    x += 1
                elif direction == "D":
                    y -= 1
                elif direction == "L":
                    x -= 1

                coordinates.append((x, y))

        lineCoordinates.append(coordinates)

    # Calculate steps taken for all intersections
    intersectionSteps = []
    line2Set = set(lineCoordinates[1])  # This speeds up membership checks
    for i, coord in enumerate(lineCoordinates[0]):
        if coord in line2Set:
            # Add 2 to account for 0-indexing in both arrays
            intersectionSteps.append(i + lineCoordinates[1].index(coord) + 2)

    # The solution is the intersection with the least combined steps
    print("RESULT:", min(intersectionSteps))


# Execute cli function on main
if __name__ == "__main__":
    main()
