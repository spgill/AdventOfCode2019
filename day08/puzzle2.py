# stdlib imports
import sys

# vendor imports
import click


blocks = {"0": " ", "1": "█"}


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("image_width", type=int)
@click.argument("image_height", type=int)
def main(input_file, image_width, image_height):
    """Put your puzzle execution code here"""
    # Load the image data string
    imageData = input_file.read().strip()

    # Split the string into layers
    layerSize = image_width * image_height
    layerData = [
        imageData[layerSize * i : layerSize * (i + 1)]
        for i in range(len(imageData) // layerSize)
    ]

    # Iterate through the size of the image and multiplex the layers
    # into the final image
    for y in range(image_height):
        for x in range(image_width):
            address = image_width * y + x
            pixel = None

            # Iterate through each layer for the pixel value
            for layer in layerData:
                pixel = layer[address]
                if pixel != "2":
                    break

            # Print the pixel to the console
            sys.stdout.write(blocks[pixel])
        sys.stdout.write("\n")

    print()


# Execute cli function on main
if __name__ == "__main__":
    main()
