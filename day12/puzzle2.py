# stdlib imports
import copy
import itertools
import math
import re
import types

# vendor imports
import click


# Convenience function for calculating Least Common Multiple
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    # Print warning
    print("WARNING: This may take a while")

    # Read the input file and parse out the vectors
    moons = [
        types.SimpleNamespace(
            pos=(int(match[0]), int(match[1]), int(match[2])), vel=(0, 0, 0),
        )
        for match in re.findall(
            r"^\D+?(-?\d+)\D+?(-?\d+)\D+?(-?\d+)",
            input_file.read().strip(),
            re.MULTILINE,
        )
    ]

    # Make a copy of the initial state for comparison
    initialMoons = copy.deepcopy(moons)

    # Iterate indefinitely to find the rotational periods for each axis
    periods = [None, None, None]
    n = 1
    while True:
        # We first update velocities by iterating through all possible pairs
        for moonA, moonB in itertools.combinations(moons, 2):
            moonA.vel = tuple(
                vel
                + (
                    0
                    if moonA.pos[i] == moonB.pos[i]
                    else math.copysign(1, moonB.pos[i] - moonA.pos[i])
                )
                for i, vel in enumerate(moonA.vel)
            )
            moonB.vel = tuple(
                vel
                + (
                    0
                    if moonB.pos[i] == moonA.pos[i]
                    else math.copysign(1, moonA.pos[i] - moonB.pos[i])
                )
                for i, vel in enumerate(moonB.vel)
            )

        # Now increment the positions by the velocities
        for moon in moons:
            moon.pos = tuple(moon.pos[i] + moon.vel[i] for i in range(3))

        # Increment loop counter
        n += 1

        # Check for repeating axises
        for axis in range(3):
            matches = 0
            for i, moon in enumerate(moons):
                if moon.pos[axis] == initialMoons[i].pos[axis]:
                    matches += 1
            if matches == len(moons) and periods[axis] is None:
                periods[axis] = n

        # If all periods have been found, break the loop
        if None not in periods:
            break

    print("RESULT:", lcm(lcm(periods[0], periods[1]), periods[2]))


# Execute cli function on main
if __name__ == "__main__":
    main()
