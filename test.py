from src.maze import MazeGenerator
from src.renderer import MazeRenderer

generator = MazeGenerator(
    rows=20,
    cols=20,
    entry=(1, 1),
    exit=(19, 14),
    perfect=True,
    seed=42,
    output_file="out_maze.txt"
)

generator.generate()

renderer = MazeRenderer(generator.grid)
renderer.show()