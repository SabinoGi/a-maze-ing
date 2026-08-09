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


####### class wal, cell -> cell.py



class MazeBacktrack:
    """Escava os caminhos do labirinto usando uma pilha e decisões claras em loop."""

    def __init__(self, grid: Grid, rng: random.Random) -> None:
        self.grid = grid
        self.rng = rng

    def _get_free_neighbors(self, cell: Cell) -> list[Cell]:
        """Returns only the neighbors that have NOT yet been visited.."""
        free_neighbors: list[Cell] = []
        
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # Norte, Sul, Leste, Oest

        for d_line, d_coluna in directions:
            new_line = cell.row + d_line
            new_colun = cell.col + d_coluna

            if self.grid.is_valid(new_line, new_colun):
                neighbors = self.grid.get(new_line, new_colun)
                
                if not neighbors.visited:
                    free_neighbors.append(neighbors)

        return free_neighbors

    def carve(self, start_row: int, start_col: int) -> None:
        """Executes the main carving loop (Move Forward and Carve or Backtrack)."""

        #Starting point
        start_cell = self.grid.get(start_row, start_col)
        start_cell.visited = True

        stack: list[Cell] = [start_cell]

        #Backtracking loop
        while len(stack) > 0:
            current_cell = stack[-1]

            unvisited_neighbors = self._find_unvisited_neighbors(current_cell)

            if len(unvisited_neighbors) > 0:
                next_cell = self.rng.choice(unvisited_neighbors)

                self.grid.connect(current_cell, next_cell)

                next_cell.visited = True
                stack.append(next_cell)

            else:
                stack.pop()


class Pattern42:
    """'42' visual pattern, end verif if grade is suffient."""
 
    PATTERN: tuple[tuple[int, ...], ...] = (
        (1, 0, 1, 0, 1, 1, 1),
        (1, 0, 1, 0, 0, 0, 1),
        (1, 1, 1, 0, 1, 1, 1),
        (0, 0, 1, 0, 1, 0, 0),
        (0, 0, 1, 0, 1, 1, 1),
    )

    HEIGHT = 5
    WIDTH = 7

    @classmethod
    def can_fit(cls, grid_rows: int, grid_cols: int) -> bool:
        """Verifica se o grid tem espaço suficiente para o padrão + margens ao redor."""

        min_rows = cls.HEIGHT + 2
        min_cols = cls.WIDTH + 2
        return grid_rows >= min_rows and grid_cols >= min_cols

    @classmethod
    def apply(cls, grid: Grid) -> None:
        """Centraliza e 'carimba' o padrão 42, marcando as células afetadas."""

        start_row = (grid.rows - cls.HEIGHT)
        start_col = (grid.cols - cls.WIDTH)

        for r_offset in range(cls.HEIGHT):
            for c_offset in range(cls.WIDTH):
                if cls.PATTERN[r_offset][c_offset] == 1:
                    cell = grid.get(start_row + r_offset, start_col + c_offset)
                    cell.is_42 = True
                    cell.visited = True


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

        if Pattern42.can_fit(self.grid.rows, self.grid.cols):
            Pattern42.apply(self.grid)
            self.pattern_applied = True
        else:
            self.pattern_applied = False
            print("Insufficient dimensions to draw the '42' pattern..")

        entry_col, entry_row = self.entry
        MazeBacktrack(self.grid, self.rng).carve(entry_row, entry_col)

        if not self.perfect:
            MazePacMan(self.grid, self.rng).braid()

    def get_walls_grid(self) -> list[list[int]]:
        """Returns the grid as integers (0 to 15), each representing the closed walls."""
        return self.grid.as_int_matrix()

    def get_solution_path(self) -> list[str]:
        """Returns the shortest path between the entrance and the exit."""
        return MazeSolver(self.grid).shortest_path(self.entry, self.exit)
