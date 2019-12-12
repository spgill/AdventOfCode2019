# stdlib imports
import itertools
import math
import re
import types

# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
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

    # Iterate through 1000 steps of simulation
    for n in range(1000):
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

    # Calculate the total energy in the system
    energy = 0
    for moon in moons:
        energy += sum([abs(n) for n in moon.pos]) * sum(
            [abs(n) for n in moon.vel]
        )

    # Print the result (as an int)
    print("RESULT:", int(energy))


# Execute cli function on main
if __name__ == "__main__":
    main()
