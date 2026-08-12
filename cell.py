import random
import typing
from enum import IntFlag
from collections import deque

from pathlib import Path



class Wall(IntFlag):
    """Bitwise representation of cell walls."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Cell():
    """"A single cell of the labyrinth."""


    def __init__(self, row: int, col: int):
=======
    def __init__(self,row: int, col: int):
>>>>>>> 027146e (mazeresolver)
=======
    def __init__(self, row: int, col: int):
>>>>>>> ce88bdf (render loadinhg)
        self.row = row
        self.col = col
        self.visited = False
        self.is_42 = False

        self.walls = Wall.NORTH | Wall.EAST | Wall.SOUTH | Wall.WEST

    def has_wall(self, wall: Wall) -> bool:
        """Returns True if the specified wall is CLOSED in this cell."""
        return bool(self.walls & wall)


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

    def walls_int(self) -> list[list[int]]:
        list_walls: list[list[int]] = []



        for line in self.grid:
            line_nbr: list[int] = []

            for cell in line:
                nbr_wall = cell.walls.value
                line_nbr.append(nbr_wall)     

            list_walls.append(line_nbr)
        return list_walls


class MazeSolver:
    """Finding the shortest path between entry/exit using BFS."""

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def shortest_path(
            self, entry: tuple[int, int], exit: tuple[int, int]) -> list[str]:
        """Calculate & returns the path as list of letters 'N','E','S','W'."""

        entry_col, entry_row = entry
        exit_col, exit_row = exit
        # breakpoint()
        start_cell = self.grid.get_cell(entry_row, entry_col)
        target_cell = self.grid.get_cell(exit_row, exit_col)

        movements = [
            (-1, 0, Wall.NORTH, 'N'),
            (1, 0, Wall.SOUTH, 'S'),
            (0, 1, Wall.EAST, 'E'),
            (0, -1, Wall.WEST, 'W')
        ]

        queue = deque([(start_cell, [])])
        visited = {start_cell}
        while len(queue) > 0:
            current_cell, current_path = queue.popleft()

            if current_cell == target_cell:
                return current_path

            for row_delta, column_delta, blocking_wall, direction in movements:

                if current_cell.has_wall(blocking_wall):
                    continue

                new_row = current_cell.row + row_delta
                new_column = current_cell.col + column_delta

                if self.grid.is_valid_pos(new_row, new_column):
                    neighbor = self.grid.get_cell(new_row, new_column)

                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = current_path + [direction]
                        queue.append((neighbor, new_path))


        for line in self.grid:
            line_nbr: list[int] = []

            for cell in line:
                nbr_wall = cell.walls.value
                line_nbr.append(nbr_wall)     

            list_walls.append(line_nbr)
        return list_walls


class MazeSolver:
    """Finding the shortest path between entry/exit using BFS."""

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def shortest_path(
            self, entry: tuple[int, int], exit: tuple[int, int]) -> list[str]:
        """Calculate & returns the path as list of letters 'N','E','S','W'."""

        entry_col, entry_row = entry
        exit_col, exit_row = exit
        # breakpoint()
        start_cell = self.grid.get_cell(entry_row, entry_col)
        target_cell = self.grid.get_cell(exit_row, exit_col)

        movements = [
            (-1, 0, Wall.NORTH, 'N'),
            (1, 0, Wall.SOUTH, 'S'),
            (0, 1, Wall.EAST, 'E'),
            (0, -1, Wall.WEST, 'W')
        ]

        queue = deque([(start_cell, [])])
        visited = {start_cell}
        while len(queue) > 0:
            current_cell, current_path = queue.popleft()

            if current_cell == target_cell:
                return current_path

            for row_delta, column_delta, blocking_wall, direction in movements:

                if current_cell.has_wall(blocking_wall):
                    continue

                new_row = current_cell.row + row_delta
                new_column = current_cell.col + column_delta

                if self.grid.is_valid_pos(new_row, new_column):
                    neighbor = self.grid.get_cell(new_row, new_column)

                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = current_path + [direction]
                        queue.append((neighbor, new_path))

        return []


=======
>>>>>>> 243491e (mazebacktrack ok)
class MazePacMan:
    def __init__(self, grid: Grid, rng: random.Random) -> None:
        self.grid = grid
        self.rng = rng

    def _is_dead_end(self, cell: Cell) -> bool:
        close_walls = cell.walls.value.bit_count()
        return close_walls >= 3

    def _get_neighbor_open(self, cell: Cell) -> list[Cell]:
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


                    available_neighbors = self._get_neighbor_open(current_cell)

                    if available_neighbors:
                        selected_neighbor = self.rng.choice(
                            available_neighbors)

                        self.grid.connect(current_cell, selected_neighbor)




                    available_neighbors = self._get_neighbors_to_open(current_cell)

                    available_neighbors = self._get_neighbor_open(current_cell)


                    if available_neighbors:
                        selected_neighbor = self.rng.choice(
                            available_neighbors)

                        self.grid.connect(current_cell, selected_neighbor)


>>>>>>> 243491e (mazebacktrack ok)
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
        """Executes carving loop (Move Forward and Carve or Backtrack)"""

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
        """Checks if grid has enough space for the pattern +margins.."""

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
                    cell = grid.get_cell(
                        start_row + r_offset, start_col + c_offset)

                    cell.is_42 = True
                    cell.visited = True


class MazeGenerator:
    """Lead orchestrator responsible for integrating the generation."""
    def __init__(
        self, rows: int, cols: int, entry: tuple[int, int],


        exit: tuple[int, int], perfect: bool,
            seed: int | None = None, 
            output_file: str = "maze.txt") -> None:

        exit: tuple[int, int], perfect: bool = False,
=======
        exit: tuple[int, int], perfect: bool,

            seed: int | None = None) -> None:
>>>>>>> b86f004 (new seed)

        self.grid = Grid(rows, cols)
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.output_file = output_file
        self.pattern_applied = False

    def generate(self) -> None:
        """Executes generation:'42' pattern, excavation, and loops."""

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
        Consolidates the wall matrix and the solution path into a single method.
        Returns: (matrix_of_integers, list_of_directions)
        """
        grid_maze = self.grid.walls_int()

        row = self.exit[0] - 1
        col = self.exit[1] - 1
        solution_path = MazeSolver(self.grid).shortest_path(self.entry, [row, col])
        return grid_maze, solution_path
=======
    # def get_walls_grid(self) -> list[list[int]]:
    #    """Returns the grid as integers (0 to 15), each representing the closed walls."""
    #    return self.grid.as_int_matrix()
=======
    def get_walls_grid(self) -> list[list[int]]:
        """Returns the grid  (0-15), each representing the closed walls."""
        return self.grid.walls_int()
>>>>>>> 027146e (mazeresolver)

<<<<<<< HEAD
    # def get_solution_path(self) -> list[str]:
        # """Returns the shortest path between the entrance and the exit."""
        # return MazeSolver(self.grid).shortest_path(self.entry, self.exit)
>>>>>>> 916fa57 (color 42)

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

            entry_x, entry_y = self.entry
            exit_x, exit_y = self.exit

            f.write(f"{entry_x},{entry_y}\t\tentry (x,y)\n")
            f.write(f"{exit_x},{exit_y}\t\texit  (x,y)\n")

            path_string = "".join(solution_path)
            f.write(f"{path_string}\n")
=======
    def get_solution_path(self) -> list[str]:
        """Returns the shortest path between the entrance and the exit."""
        row = self.exit[0] - 1
        col = self.exit[1] - 1
        return MazeSolver(self.grid).shortest_path(self.entry, [row, col])


class MazeRenderer:
    def __init__(self, grid: Grid):
        self.grid = grid

    def export(maze: list[list[int]], file_name: str) -> None:
        file: typing.IO[str] | None = None

        try:
            file = open(file_name, "w")

            for i in maze:
                for j in i:
                    file.write(f"{j:x}")

        except PermissionError as error:
            print(f"Error writing file '{file}': {error}")
            return 0
        finally:
            if file is not None:
                file.close()
>>>>>>> ce88bdf (render loadinhg)



class MazeRenderer:
    def __init__(self, grid: Grid):
        self.grid = grid

    def export(maze: list[list[int]], file_name: str) -> None:
        file: typing.IO[str] | None = None

<<<<<<< HEAD
# def show_maze(grid):
#    for row in range(grid.rows):
>>>>>>> b86f004 (new seed)

        try:
            file = open(file_name, "w")

            for i in maze:
                for j in i:
                    file.write(f"{j:x}")

        except PermissionError as error:
            print(f"Error writing file '{file}': {error}")
            return 0
        finally:
            if file is not None:
                file.close()


def show_maze(grid):
    for row in range(grid.rows):

        # Linha superior
        for col in range(grid.cols):
            cell = grid.get_cell(row, col)

# def main():
#    grid = Grid(5, 5)

#    rng = random.Random(55)
>>>>>>> b86f004 (new seed)

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
        rows=20,
        cols=20,
        entry=(1, 1),
        exit=(19, 14),
        perfect=True,
        seed=42,
        output_file="out_maze.txt"
    )

    generator.generate()

    generator.write_file()

    # show_maze(generator.grid)


if __name__ == "__main__":
    main()

    """
    Generate and solve a maze.

    Args:
        rows: Number of rows.
        cols: Number of columns.
        entry: Entry coordinates as (x, y).
        exit: Exit coordinates as (x, y).
        perfect: If True, generates a perfect maze.
        seed: Optional seed for deterministic generation.

    Example:
        generator = MazeGenerator(
            rows=20,
            cols=20,
            entry=(0, 0),
            exit=(19, 19),
            perfect=True,
            seed=42
        )

        generator.generate()

        maze = generator.get_walls_grid()
        solution = generator.get_solution_path()
    """
=======
# if __name__ == "__main__":
#    main()
>>>>>>> b86f004 (new seed)
=======
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
        rows=20,
        cols=20,
        entry=(1, 1),
        exit=(10, 10),
        perfect=True,
        seed=42
    )

    generator.generate()

    out_maze = generator.get_walls_grid()

    file: str = "maze.txt"
    MazeRenderer.export(out_maze, file)

    # show_maze(generator.grid)


if __name__ == "__main__":
    main()
