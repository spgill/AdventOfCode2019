# stdlib imports
import math

# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    # Split the input file into lines
    modules = input_file.read().strip().splitlines()

    # Iterate through each module's mass and calculate the fuel requirements
    fuelRequirements = []
    for module in modules:
        mass = int(module)
        fuelRequirements.append(math.floor(mass / 3) - 2)

    # Print the result (the sum)
    print("RESULT:", sum(fuelRequirements))


# Execute cli function on main
if __name__ == "__main__":
    main()
