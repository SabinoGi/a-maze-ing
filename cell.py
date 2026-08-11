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

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def is_valid_pos(self, row: int, col: int) -> bool:
        """Verifica se a coordenada está dentro dos limites do grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def connect(self, cell_a: Cell, cell_b: Cell) -> None:
        """Remove a parede entre duas células vizinhas."""

        row_diff = cell_b.row - cell_a.row
        col_diff = cell_b.col - cell_a.col

        if row_diff == -1 and col_diff == 0:
            """B está ao norte de A"""
            cell_a.walls &= ~Wall.NORTH
            cell_b.walls &= ~Wall.SOUTH

        elif row_diff == 1 and col_diff == 0:
            """B está ao sul de A"""
            cell_a.walls &= ~Wall.SOUTH
            cell_b.walls &= ~Wall.NORTH

        elif row_diff == 0 and col_diff == 1:
            """B está a leste de A"""
            cell_a.walls &= ~Wall.EAST
            cell_b.walls &= ~Wall.WEST

        elif row_diff == 0 and col_diff == -1:
            """B está a oeste de A"""
            cell_a.walls &= ~Wall.WEST
            cell_b.walls &= ~Wall.EAST


class MazePacMan:
    def __init__(self, grid: Grid, rng: random.Random) -> None:
        self.grid = grid
        self.rng = rng

    def _is_dead_end(self, cell: Cell) -> bool:
        close_walls = cell.walls.value.bit_count()
        return close_walls >= 3

    def _get_neighbors_to_open(self, cell: Cell) -> list[Cell]:
        valid_neighbors: list[Cell] = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for row_offset, col_offset in directions:
            new_row = cell.row + row_offset
            new_col = cell.col + col_offset

            if self.grid.is_valid_pos(new_row, new_col):
                neighbor = self.grid.get_cell(new_row, new_col)

                if not neighbor.is_42:
                    valid_neighbors.append(neighbor)

        return valid_neighbors

    def braid(self) -> None:
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                current_cell = self.grid.get_cell(row, col)
                if current_cell.is_42:
                    continue

                if self._is_dead_end(current_cell):
                    available_neighbors = self._get_neighbors_to_open(current_cell)

                    if available_neighbors:
                        selected_neighbor = self.rng.choice(available_neighbors)
                        self.grid.connect(current_cell, selected_neighbor)


class MazeBacktrack:
    """Carve out the paths of the maze using a stack."""

    def __init__(self, grid: Grid, rng: random.Random) -> None:
        self.grid = grid
        self.rng = rng

    def _get_free_neighbors(self, cell: Cell) -> list[Cell]:
        """Returns only the neighbors that have NOT yet been visited.."""
        free_neighbors: list[Cell] = []

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for d_line, d_coluna in directions:
            new_row = cell.row + d_line
            new_col = cell.col + d_coluna

            if self.grid.is_valid_pos(new_row, new_col):
                neighbor = self.grid.get_cell(new_row, new_col)
                
                if not neighbor.visited:
                    free_neighbors.append(neighbor)

        return free_neighbors

    def carve(self, start_row: int, start_col: int) -> None:
        """Executes the main carving loop (Move Forward and Carve or Backtrack)."""

        start_cell = self.grid.get_cell(start_row, start_col)
        start_cell.visited = True

        stack: list[Cell] = [start_cell]

        while len(stack) > 0:
            current_cell = stack[-1]

            unvisited_neighbors = self._get_free_neighbors(current_cell)

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
        (1, 0, 0, 0, 1, 1, 1),
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

        start_row = (grid.rows - cls.HEIGHT) // 2
        start_col = (grid.cols - cls.WIDTH) // 2

        for r_offset in range(cls.HEIGHT):
            for c_offset in range(cls.WIDTH):
                if cls.PATTERN[r_offset][c_offset] == 1:
                    cell = grid.get_cell(start_row + r_offset, start_col + c_offset)
                    cell.is_42 = True
                    cell.visited = True


class MazeGenerator:
    """Lead orchestrator responsible for integrating the generation."""
    def __init__(
        self, rows: int, cols: int, entry: tuple[int, int],
        exit: tuple[int, int], perfect: bool,
            seed: int | None = None) -> None:

        self.grid = Grid(rows, cols)
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.pattern_applied = False

    def generate(self) -> None:
        """Executes generation:'42' pattern, excavation, and loops."""

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

    # def get_walls_grid(self) -> list[list[int]]:
    #    """Returns the grid as integers (0 to 15), each representing the closed walls."""
    #    return self.grid.as_int_matrix()

    # def get_solution_path(self) -> list[str]:
        # """Returns the shortest path between the entrance and the exit."""
        # return MazeSolver(self.grid).shortest_path(self.entry, self.exit)


def show_maze(grid):
    for row in range(grid.rows):

        # Linha superior
        for col in range(grid.cols):
            cell = grid.get_cell(row, col)

            if cell.walls & Wall.NORTH:
                print("+---", end="")
            else:
                print("+   ", end="")

        print("+")

        # Conteúdo + paredes laterais
        for col in range(grid.cols):
            cell = grid.get_cell(row, col)

            if cell.walls & Wall.WEST:
                print("|", end="")
            else:
                print(" ", end="")

            if cell.is_42:
                print("\033[41m   \033[0m", end="")
            else:
                print("   ", end="")

        # Parede direita
        cell = grid.get_cell(row, grid.cols - 1)

        if cell.walls & Wall.EAST:
            print("|")
        else:
            print(" ")

    # Linha inferior
    for col in range(grid.cols):
        cell = grid.get_cell(grid.rows - 1, col)

        if cell.walls & Wall.SOUTH:
            print("+---", end="")
        else:
            print("+   ", end="")

    print("+")


def main():
    generator = MazeGenerator(
        rows=10,
        cols=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=None
    )

    generator.generate()

    show_maze(generator.grid)


if __name__ == "__main__":
    main()