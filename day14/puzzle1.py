# stdlib imports
import collections
import math
import pprint

# vendor imports
import click


Reaction = collections.namedtuple("Reaction", ["reactants", "product"])
Factor = collections.namedtuple("Factor", ["quantity", "name"])


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    # Read the reaction list and decode it
    reactions = []
    for line in input_file.read().strip().splitlines():
        # Split reaction line into reactants and products
        reactants, product = line.split(" => ")

        # Split all reactants into Factor objects
        reactants = tuple(
            Factor(int(quantity), name)
            for quantity, name in map(
                lambda r: r.split(" "), reactants.split(", ")
            )
        )

        # Convert the product into a Factor object
        product = product.split(" ")
        product = Factor(int(product[0]), product[1])

        # Add the decoded reaction line to the pile
        reactions.append(Reaction(reactants, product))

    # Find the primitive reaction (ones that are produced directly from ore)
    primitives = set(
        reaction.product.name
        for reaction in filter(
            lambda reaction: reaction.reactants[0].name == "ORE", reactions
        )
    )
    primitiveCount = {name: 0 for name in primitives}

    # Resolve the requirements for one unit of fuel, in relation to primitives
    def resolveOreRequirement(reactionList, desiredName):
        # Find the reaction that produces the desired product
        reaction = list(
            filter(lambda r: r.product.name == desiredName, reactionList)
        )[0]

        # If the sole reactant is ORE, then we've reached maximum recursion
        # if (
        #     len(reaction.reactants) == 1
        #     and reaction.reactants[0].name == "ORE"
        # ):
        #     return reaction.reactants[0].quantity / reaction.product.quantity

        # # Else, iterate over all the reactants and find the common multiple
        # total = 0
        # for factor in reaction.reactants:
        #     total += resolveOreRequirement(reactionList, factor.name)
        # return total / reaction.product.quantity

        for factor in reaction.reactants:
            if factor.name in primitives:
                primitiveCount[factor.name] += (
                    factor.quantity / reaction.product.quantity
                )
                continue
            resolveOreRequirement(reactionList, factor.name)

    resolveOreRequirement(reactions, "FUEL")
    print(primitiveCount)

    total = 0
    for primitiveName in primitives:
        reaction = list(
            filter(lambda r: r.product.name == primitiveName, reactions)
        )[0]

        total += (
            primitiveCount[primitiveName] / reaction.product.quantity
        ) * reaction.reactants[0].quantity
    print(total)


# Execute cli function on main
if __name__ == "__main__":
    main()
