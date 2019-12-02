# vendor imports
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    """Put your puzzle execution code here"""
    print(input_file)


# Execute cli function on main
if __name__ == "__main__":
    main()
