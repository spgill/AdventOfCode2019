# stdlib imports
import math

# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Read the map and split it into lines.
    # Make sure to access it like this `mapData[y][x]`
    mapData = input_file.read().strip().splitlines()
    mapWidth = len(mapData[0])
    mapHeight = len(mapData)

    # Iterate through each point on the map
    slopeCounts = []
    for y in range(mapHeight):
        for x in range(mapWidth):
            obj = mapData[y][x]

            # If the current position is empty, skip it
            if obj == ".":
                continue

            # Iterate through each OTHER point on the map and calculate its
            # slope from the station point
            slopes = set()
            for y2 in range(mapHeight):
                for x2 in range(mapWidth):
                    # Make sure to skip the station point and the empty points
                    if x2 == x and y2 == y or mapData[y2][x2] == ".":
                        continue
                    slopes.add(
                        (
                            (y2 - y) / (x2 - x) if x2 != x else math.inf,
                            math.copysign(1.0, x2 - x),
                            math.copysign(1.0, y2 - y),
                        )
                    )

            slopeCounts.append((len(slopes), x, y))

    # Print the location of the station (useful for verifying part 2),
    # and print the actual result
    result = max(slopeCounts, key=lambda s: s[0])
    print("STATION AT", (result[1], result[2]))
    print("RESULT:", result[0])


# Execute cli function on main
if __name__ == "__main__":
    main()
