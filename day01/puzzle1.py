# stdlib imports
import math

# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    modules = input_file.read().strip().splitlines()
    fuelRequirements = []

    for module in modules:
        mass = int(module)
        fuelRequirements.append(math.floor(mass / 3) - 2)

    print("RESULT:", sum(fuelRequirements))


# Execute cli function on main
if __name__ == "__main__":
    main()
