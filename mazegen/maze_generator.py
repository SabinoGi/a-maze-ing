import sys
import random
from maze import Grid
from pathlib import Path
from maze_utils import Pattern42, MazeSolver
from maze_backtrack import MazeBacktrack, MazePacMan


class MazeGenerator:
    """Lead orchestrator responsible for integrating the generation."""

    def __init__(
        self,
        rows: int,
        cols: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
        output_file: str = "maze.txt"
    ) -> None:

        errors = []
        if rows <= 0:
            errors.append("Rows must be greater than 0")
        if cols <= 0:
            errors.append("Cols must be greater than 0")
        if not (0 <= entry[0] < cols and 0 <= entry[1] < rows):
            errors.append("Invalid entry position")
        if not (0 <= exit[0] < cols and 0 <= exit[1] < rows):
            errors.append("Invalid exit position")
        if entry == exit:
            errors.append("Entry and exit must be different")
        if not isinstance(perfect, bool):
            errors.append("Perfect must be a boolean")
        if seed is not None and not isinstance(seed, int):
            errors.append("Seed must be an integer or None")
        if not isinstance(output_file, str):
            errors.append("Output file must be a non-empty string")
        try:
            if len(errors) > 0:
                raise ValueError(errors)
            self.rows = rows
            self.cols = cols
            self.seed = seed
            self.grid = Grid(rows, cols)
            self.entry_xy = entry
            self.exit_xy = exit
            self.entry = (entry[1], entry[0])
            self.exit = (exit[1], exit[0])
            self.perfect = perfect
            self.rng = random.Random(seed)
            self.output_file = output_file
            self.pattern_applied = False
        except ValueError as e:
            for error in e.args[0]:
                print(f"Error: {error}")
            sys.exit(1)

    def generate(self) -> None:
        """Executes generation:'42' pattern, excavation, and loops."""
        self.grid = Grid(self.rows, self.cols)

        if self.seed is None:
            self.rng = random.Random(None)

        if Pattern42.can_fit(self.grid.rows, self.grid.cols):
            Pattern42.apply(self.grid)
            self.pattern_applied = True
        else:
            self.pattern_applied = False
            print("Insufficient dimensions to draw the '42' pattern..\n")

        entry_col, entry_row = self.entry
        MazeBacktrack(self.grid, self.rng).carve(entry_row, entry_col)

        if not self.perfect:
            MazePacMan(self.grid, self.rng).braid()

    def get_maze_data(self) -> tuple[list[list[int]], list[str]]:
        """
        Consolidates the wall matrix and the solution path into
          a single method. Returns: (matrix_of_integers, list_of_directions)
        """
        grid_maze = self.grid.walls_int()

        solution_path = MazeSolver(self.grid).shortest_path(
            self.entry, self.exit)
        return grid_maze, solution_path

    def write_file(self) -> None:
        """
        Gets the maze and solution data and writes it to the
         file in the exact format specified:
        - Walls in hexadecimal format (0-f), one row per line
        - Blank line
        - Entry and exit coordinates
        - Continuous string representing the solution path
        """
        path_file = Path(self.output_file if self.output_file else "maze.txt")

        if path_file.parent:
            path_file.parent.mkdir(parents=True, exist_ok=True)

        grid_matrix, solution_path = self.get_maze_data()

        with open(path_file, "w", encoding="utf-8") as f:

            for row in grid_matrix:
                row_hex = "".join(f"{value:x}" for value in row)
                f.write(f"{row_hex}\n")

            f.write("\n")

            f.write(f"{self.entry_xy[0]},{self.entry_xy[1]}\n")
            f.write(f"{self.exit_xy[0]},{self.exit_xy[1]}\n")

            path_string = "".join(solution_path)
            f.write(f"{path_string}\n")


def main() -> None:
    generator = MazeGenerator(
        rows=10,
        cols=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=None,
        output_file=""
    )

    generator.generate()

    generator.write_file()

    # render = MazeRender(generator)
    # render.render()
    # render.interaction()


if __name__ == "__main__":
    main()
