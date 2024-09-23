from cnegng.ACME.spatial2d import Grid, Position
from cnegng.generations.one import Sprite

class Spatial2DGraphvizRenderer:
    def __init__(self):
        self.output = []

    def render(self, obj):
        """Main entry point to render a spatial2d object."""
        if isinstance(obj, Grid):
            return self._render_grid(obj)
        elif isinstance(obj, Position):
            return self._render_position(obj)
        elif isinstance(obj, Sprite):
            return self._render_sprite(obj)
        else:
            raise TypeError(f"Unsupported object type: {type(obj)}")

    def _render_grid(self, grid: Grid):
        """Render a Grid object as a grid in Graphviz, labeling intersections with coordinates."""
        self.output.append("digraph G {")
        self.output.append("  node [shape=box];")
        self.output.append("  graph [splines=false];")

        num_rows = len(grid.cells)
        num_cols = len(grid.cells[0])

        # Render the cells in the grid with coordinate labels
        for row_index in range(num_rows):
            for col_index in range(num_cols):
                cell = grid.cells[row_index][col_index]
                label = f"({col_index}, {row_index})"
                self.output.append(f'  cell_{row_index}_{col_index} [label="{label}", pos="{col_index},{-row_index}!"];')

        # Render grid structure
        for row_index in range(num_rows):
            for col_index in range(num_cols - 1):
                self.output.append(f'  cell_{row_index}_{col_index} -> cell_{row_index}_{col_index + 1} [dir=none];')
        for col_index in range(num_cols):
            for row_index in range(num_rows - 1):
                self.output.append(f'  cell_{row_index}_{col_index} -> cell_{row_index + 1}_{col_index} [dir=none];')

    def _render_position(self, position: Position):
        """Render a Position object on the grid."""
        self.output.append(f'  pos_{position.x}_{position.y} [label="({position.x}, {position.y})", pos="{position.x},{-position.y}!"];')

    def _render_sprite(self, sprite: Sprite):
        """Render a Sprite object on the grid with its texture label."""
        label = sprite.texture_name  # Assuming the texture name is stored as texture_name
        position = sprite.position
        self.output.append(f'  sprite_{position.x}_{position.y} [label="{label}", pos="{position.x},{-position.y}!"];')

    def _reset(self):
        """Reset the output buffer."""
        self.output = []

    def render_full_grid_with_positions_and_sprites(self, grid: Grid, positions, sprites):
        """Render the grid and overlay positions and sprites."""
        self._reset()
        self._render_grid(grid)

        for pos in positions:
            self._render_position(pos)

        for sprite in sprites:
            self._render_sprite(sprite)

        self.output.append("}")
        return "\n".join(self.output)
