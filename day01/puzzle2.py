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

        moduleFuelReq = math.floor(mass / 3) - 2
        fuelRequirements.append(moduleFuelReq)
        print("MODULE", moduleFuelReq)

        fuelReqCounter = moduleFuelReq
        while True:
            req = math.floor(fuelReqCounter / 3) - 2
            print("   ", req)
            if req <= 0:
                break
            fuelRequirements.append(req)
            fuelReqCounter = req

    print("RESULT:", sum(fuelRequirements))


# Execute cli function on main
if __name__ == "__main__":
    main()
