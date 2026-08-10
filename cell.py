import random
from enum import IntFlag


class Wall(IntFlag):
    """Bitwise representation of cell walls."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Cell():
    """"A single cell of the labyrinth."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.is_42 = False

        self.walls = Wall.NORTH | Wall.EAST | Wall.SOUTH | Wall.WEST


class Grid():
    """Labyrinth cell structure and basic operations on them."""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Cell]] = [
            [Cell(r, c) for c in range(cols)]
            for r in range(rows)
        ]

    def is_valid_pos(self, row: int, col: int) -> bool:
        """Verifica se a coordenada está dentro dos limites do grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols


class Pattern42:
    """'42' visual pattern, end verif if grade is suffient."""
 
    PATTERN: tuple[tuple[int, ...], ...] = (
        (1, 0, 1, 0, 1, 1, 1),
        (1, 0, 1, 0, 0, 0, 1),
        (1, 1, 1, 0, 1, 1, 1),
        (0, 0, 1, 0, 1, 0, 0),
        (0, 0, 1, 0, 1, 1, 1),
    )

    @staticmethod
    def is_suffient(rows, cols):
        pattern_rows = len(Pattern42.PATTERN)
        pattern_cols = len(Pattern42.PATTERN[0])

        if rows < pattern_rows or cols < pattern_cols:
            return None

        return Pattern42.PATTERN

class MazeGenerator:
    """Lead orchestrator responsible for integrating the generation pipeline."""
    def __init__(
        self, rows: int, cols: int, entry: tuple[int, int],
        exit: tuple[int, int], perfect: bool = False,
        seed: Optional[int] = None) -> None:

        self.grid = Grid(rows, cols)
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.pattern_applied = False


    def generate(self) -> None:
        """Executa todo o pipeline de geração: padrão '42', escavação e (se aplicável) loops."""

        self.is_pattern42 = Pattern42.apply(self.grid)
        entry_col = self.entry[0]
        entry_row = self.entry[1]

        if not self.pattern_applied:
            print("Insufficient dimensions to draw the '42' pattern..")

        MazeBacktrak(self.grid, entry_row, entry_col)

        if not self.perfect:
            MazePacMan(self.grid, self.rng).braid()

    def get_walls_grid(self) -> list[list[int]]:
        """Returns the grid as integers (0 to 15), each representing the closed walls."""
        return self.grid.as_int_matrix()

    def get_solution_path(self) -> list[str]:
        """Returns the shortest path between the entrance and the exit."""
        return MazeSolver(self.grid).shortest_path(self.entry, self.exit)