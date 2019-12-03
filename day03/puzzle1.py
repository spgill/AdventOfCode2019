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
        coordinates = set()

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

                coordinates.add((x, y))

        lineCoordinates.append(coordinates)

    # Look for entries common to both sets and calculate distance from origin
    intersections = []
    for coord in lineCoordinates[0]:
        if coord in lineCoordinates[1]:
            intersections.append(abs(coord[0]) + abs(coord[1]))

    # The solution is the closest intersection
    print("RESULT:", min(intersections))


# Execute cli function on main
if __name__ == "__main__":
    main()
