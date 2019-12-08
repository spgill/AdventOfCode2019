# vendor imports
import click


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

    # Count the digits in the layers
    layerCounts = [
        (layer.count("0"), layer.count("1") * layer.count("2"))
        for layer in layerData
    ]

    # The result is the layer with the least 0's, and the count of that
    # layer's 1's and 2's multiplied
    print("RESULT:", min(layerCounts, key=lambda l: l[0])[1])


# Execute cli function on main
if __name__ == "__main__":
    main()
