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

        moduleFuelReq = math.floor(mass / 3) - 2
        fuelRequirements.append(moduleFuelReq)

        # Each unit of fuel has it's own fuel requirements.
        # Recursively calculate the fuel's fuel requirement until the
        # return is negligible.
        fuelReqCounter = moduleFuelReq
        while True:
            req = math.floor(fuelReqCounter / 3) - 2
            if req <= 0:
                break
            fuelRequirements.append(req)
            fuelReqCounter = req

    # Print the result (the sum of EVERYTHING)
    print("RESULT:", sum(fuelRequirements))


# Execute cli function on main
if __name__ == "__main__":
    main()
