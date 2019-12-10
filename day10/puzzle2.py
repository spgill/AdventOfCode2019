# stdlib imports
import collections
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

    # We need the results of part 1 to solve this
    resultP1 = max(slopeCounts, key=lambda s: s[0])

    # Condense the asteroids down to a list and sort it based on distance
    # to the station
    station = (resultP1[1], resultP1[2])
    print("STATION AT", station)
    asteroids = []
    for y in range(mapHeight):
        for x in range(mapWidth):
            obj = mapData[y][x]
            if obj == "#" and (x, y) != station:
                asteroids.append((x, y))
    asteroids.sort(
        key=lambda coord: math.hypot(
            coord[0] - station[0], coord[1] - station[1]
        )
    )

    # Group the asteroids by cardinality and slope
    groups = dict()
    for target in asteroids:
        slope = (
            (target[1] - station[1]) / (target[0] - station[0])
            if target[0] != station[0]
            else math.inf
        )
        cardinalX = math.copysign(1.0, target[0] - station[0])
        cardinalY = math.copysign(1.0, target[1] - station[1])

        if (cardinalX, cardinalY) not in groups:
            groups[(cardinalX, cardinalY)] = collections.defaultdict(list)

        # Vertical or horizontal points are subgrouped together
        if slope == math.inf or slope == 0:
            subgroup = slope
        else:
            subgroup = abs(slope) ** (cardinalX * cardinalY)
            # subgroup = math.copysign(slope, cardinalX * cardinalY)

        # Add the asteroid to its group and subgroup
        groups[(cardinalX, cardinalY)][subgroup].append(target)

    # Iterate through the groups in clockwise order, popping off
    # asteroids to find the 200th
    count = 0
    found = None
    while found is None:
        for direction in [
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]:
            if direction in groups:
                for slope, targets in sorted(
                    groups[direction].items(), key=lambda item: item[0]
                ):
                    if len(targets):
                        target = targets.pop(0)
                        count += 1
                        if count == 200:
                            found = target

    print("RESULT:", found[0] * 100 + found[1])


# Execute cli function on main
if __name__ == "__main__":
    main()
