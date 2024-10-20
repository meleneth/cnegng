import os
import subprocess
import tempfile

from cnegng.ACME.spatial2d import Area, Dimensions, Grid, Position
from cnegng.generations.one import Sprite, Spatial2DGraphvizRenderer


def render_graphviz_and_display(graphviz_str):
    """Render the Graphviz string using dot and display the result inline in Alacritty."""

    # Create a temporary file for the Graphviz input (DOT format)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dot") as dot_file:
        dot_file.write(graphviz_str.encode("utf-8"))
        dot_file_name = dot_file.name

    # Create a temporary file for the output image (PNG format)
    output_image = dot_file_name.replace(".dot", ".png")

    try:
        # Generate the image using `dot`
        subprocess.run(["dot", "-Tpng", dot_file_name, "-o", output_image], check=True)

        # Display the image inline in Alacritty
        # Alacritty uses `kitty` image protocol for inline images
        print(
            f"\033]1337;File=inline=1;width=auto;height=auto;preserveAspectRatio=1:{output_image}\a"
        )

    finally:
        # Clean up temporary files
        os.remove(dot_file_name)
        os.remove(output_image)


if __name__ == "__main__":
    # Example: Generate a Graphviz DOT string from some spatial2d objects
    grid_area = Area(0, 0, 100, 100)
    dimensions = Dimensions(10, 10)
    grid = Grid(grid_area, dimensions)

    positions = [Position(2, 3), Position(6, 6)]
    sprites = [Sprite(Position(4, 5), "texture1"), Sprite(Position(7, 8), "texture2")]

    renderer = Spatial2DGraphvizRenderer()
    graphviz_str = renderer.render_full_grid_with_positions_and_sprites(
        grid, positions, sprites
    )

    # Render the graphviz and display the image inline in the terminal
    render_graphviz_and_display(graphviz_str)
