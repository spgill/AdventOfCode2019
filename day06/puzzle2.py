# stdlib imports
import dataclasses
import typing

# vendor imports
import click


# Class representing a single node in the orbital tree
@dataclasses.dataclass(unsafe_hash=True)
class CelestialBody:
    name: str
    orbits: typing.Any = dataclasses.field(compare=False)
    orbitedBy: typing.Any = dataclasses.field(compare=False)


# Try and find a single node in a single tree
def findBodyInChain(chain, name):
    if chain.name == name:
        return chain

    for body in chain.orbitedBy:
        match = findBodyInChain(body, name)
        if match:
            return match


# Try and find a single node in multiple trees
def findBodyInHeads(heads, name):
    for head in heads:
        body = findBodyInChain(head, name)
        if body:
            return body


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    pairInputLines = input_file.read().strip().splitlines()

    heads = set()

    # Iterate through each line ans split the pair apart
    for pairLine in pairInputLines:
        orbiteeName, orbiterName = pairLine.split(")")

        # Try and find the orbitee's body,
        # else, create it and add it to the heads
        if not (orbiteeBody := findBodyInHeads(heads, orbiteeName)):
            orbiteeBody = CelestialBody(orbiteeName, None, [])
            heads.add(orbiteeBody)

        # Check if the orbiter already exists,
        # if it does, remove it from the heads
        # else, create a new one
        if orbiterBody := findBodyInHeads(heads, orbiterName):
            heads.remove(orbiterBody)
        else:
            orbiterBody = CelestialBody(orbiterName, orbiteeName, [])

        # Create the links
        orbiteeBody.orbitedBy.append(orbiterBody)
        orbiterBody.orbits = orbiteeBody

    # All the heads should be resolved to one
    assert len(heads) == 1
    centralBody = list(heads)[0]

    # First we have to find the starting node (YOU)
    node = findBodyInChain(centralBody, "YOU").orbits
    transfers = 0

    # Loop through children and parents until we find the damn thing
    while node.name != "SAN":
        # Is SAN a child of the current node?
        for childNode in node.orbitedBy:
            if findBodyInChain(childNode, "SAN"):
                node = childNode
                transfers += 1
                break

        # Else, move up to the parent
        else:
            node = node.orbits
            transfers += 1

    # -1 because we don't count orbitting SAN
    print("RESULT:", transfers - 1)


# Execute cli function on main
if __name__ == "__main__":
    main()
