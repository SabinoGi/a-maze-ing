import random
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

        entry_row, entry_col = entry
        exit_row, exit_col = exit

        start_cell = self.grid.get_cell(entry_row, entry_col)
        target_cell = self.grid.get_cell(exit_row, exit_col)

        movements = [
            (-1, 0, Wall.NORTH, 'N'),
            (1, 0, Wall.SOUTH, 'S'),
            (0, 1, Wall.EAST, 'E'),
            (0, -1, Wall.WEST, 'W')
        ]

        queue: deque[tuple[Cell, list[str]]] = deque([(start_cell, [])])
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


class MazePacMan:
    def __init__(self, grid: Grid, rng: random.Random) -> None:
        self.grid = grid
        self.rng = rng


    def _is_dead_end(self, cell: Cell) -> bool:
        close_walls = cell.walls.value.bit_count()
        return close_walls >= 3
=======
    def _is_dead_end(self) -> list[Cell]:
        """Identifies cells with 3 or 4 closed
        walls that are NOT part of the '42' pattern."""
        dead_ends: list[Cell] = []
>>>>>>> 472ef92 (flak8 end mypy --strict ok):cell.py

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
=======
                closed_walls = cell.walls.value.bit_count()
                if closed_walls >= 3:
                    dead_ends.append(cell)

        return dead_ends

    def _get_closed_neighbors(self, cell: Cell) -> list[Cell]:
        """Returns neighbors separated by a
        CLOSED WALL that do not match the '42' pattern."""
        closed_neighbors: list[Cell] = []

        directions = [
            (-1, 0, Wall.NORTH),
            (1, 0, Wall.SOUTH),
            (0, 1, Wall.EAST),
            (0, -1, Wall.WEST)
        ]

        for dr, dc, wall_dir in directions:
            nr, nc = cell.row + dr, cell.col + dc

            if self.grid.is_valid_pos(nr, nc):
                neighbor = self.grid.get_cell(nr, nc)

                if not neighbor.is_42 and cell.has_wall(wall_dir):
                    closed_neighbors.append(neighbor)

        return closed_neighbors

    def braid(self, max_dead_ends_tolerated: int = 2) -> None:
        """Iteratively remove dead ends until the tolerance is reached."""
        while True:
            dead_ends = self._is_dead_end()

            if len(dead_ends) <= max_dead_ends_tolerated:
                break

            self.rng.shuffle(dead_ends)
            removed_any = False

            for cell in dead_ends:
                if cell.walls.value.bit_count() < 3:
                    continue

                neighbors = self._get_closed_neighbors(cell)
                if neighbors:
                    selected_neighbor = self.rng.choice(neighbors)

                    self.grid.connect(cell, selected_neighbor)
                    removed_any = True

            if not removed_any:
                break
>>>>>>> 472ef92 (flak8 end mypy --strict ok):cell.py


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

        self.rows = rows
        self.cols = cols
        self.seed = seed
        self.grid = Grid(rows, cols)

        self.entry = entry
        self.exit = exit
=======
        self.entry_xy = entry
        self.exit_xy = exit
        self.entry = (entry[1], entry[0])
        self.exit = (exit[1], exit[0])

>>>>>>> f637046 (render ok):cell.py
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.output_file = output_file
        self.pattern_applied = False

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


        row = self.exit[0] - 1
        col = self.exit[1] - 1
        solution_path = MazeSolver(self.grid).shortest_path(self.entry, [row, col])
=======
        solution_path = MazeSolver(self.grid).shortest_path(self.entry, self.exit)

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

            entry_x, entry_y = self.entry
            exit_x, exit_y = self.exit

            f.write(f"{entry_x},{entry_y}\t\tentry (x,y)\n")
            f.write(f"{exit_x},{exit_y}\t\texit  (x,y)\n")

            path_string = "".join(solution_path)

            f.write(f"{path_string}\n")
=======
            f.write(f"{path_string}\n")


class MazeRender:
    """Renderiza o labirinto no terminal e gerencia o menu do usuário."""

    def __init__(self, generator: MazeGenerator) -> None:
        self.generator = generator
        self.show_path = False
        self.colors = [
            "\033[97m", "\033[94m", "\033[92m", "\033[93m", "\033[96m"]
        self.color_idx = 0

    def render(self) -> None:
        grid = self.generator.grid
        wall_color = self.colors[self.color_idx]

        # Estilos dos elementos
        QUINA = f"\033[1m{wall_color}■\033[0m"
        TETO = f"\033[1m{wall_color}━━━\033[0m"
        PAREDE = f"\033[1m{wall_color}┃\033[0m"
        VAZIO = "   "

        # Preenchimentos especiais
        ENTRY_BG = "\033[45m   \033[0m"    # Rosa/Magenta
        EXIT_BG = "\033[41m   \033[0m"     # Vermelho
        PATH_BG = "\033[42m   \033[0m"     # Verde
        PATTERN_BG = "\033[47m   \033[0m"  # Cinza ('42')

        # Obtém os passos da solução apenas se a opção estiver ativada
        path_positions = set()
        if self.show_path:
            path_str = MazeSolver(grid).shortest_path(
                self.generator.entry, self.generator.exit)

            r, c = self.generator.entry
            path_positions.add((r, c))
            deltas = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
            for move in path_str:
                dr, dc = deltas[move]
                r, c = r + dr, c + dc
                path_positions.add((r, c))

        # Desenho do labirinto
        for row in range(grid.rows):
            # 1. Linha superior
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                top = TETO if cell.has_wall(Wall.NORTH) else VAZIO
                print(f"{QUINA}{top}", end="")
            print(QUINA)

            # 2. Conteúdo central e paredes laterais
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                left = PAREDE if cell.has_wall(Wall.WEST) else " "

                # Define a cor de fundo da célula
                pos = (row, col)
                if pos == self.generator.entry:
                    content = ENTRY_BG
                elif pos == self.generator.exit:
                    content = EXIT_BG
                elif cell.is_42:
                    content = PATTERN_BG
                elif pos in path_positions:
                    content = PATH_BG
                else:
                    content = VAZIO

                print(f"{left}{content}", end="")

            # Parede Leste da última coluna
            last_cell = grid.get_cell(row, grid.cols - 1)
            right = PAREDE if last_cell.has_wall(Wall.EAST) else " "
            print(right)

        # 3. Linha inferior da última fileira
        for col in range(grid.cols):
            cell = grid.get_cell(grid.rows - 1, col)
            bottom = TETO if cell.has_wall(Wall.SOUTH) else VAZIO
            print(f"{QUINA}{bottom}", end="")
        print(QUINA)

    def interaction(self) -> None:
        """Exibe o menu sem módulos externos."""
        error_msg = ""

        while True:
            # 1. Limpa o terminal e renderiza o labirinto atual
            print("\033[H\033[2J", end="")
            self.render()

            # 2. Se houver erro de digitação anterior, exibe agora
            if error_msg:
                print(f"\n\033[91m{error_msg}\033[0m")
                error_msg = ""

            # 3. Exibe o menu
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show / Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")

            try:
                choice = input("\033[92mChoice? (1-4): \033[0m").strip()

                if choice == "1":
                    # Cria novo labirinto na memória e salva no arquivo
                    self.generator.generate()
                    self.generator.write_file()
                    # Na próxima volta do loop, render() desenhará o NOVO grid
                elif choice == "2":
                    self.show_path = not self.show_path
                elif choice == "3":
                    self.color_idx = (self.color_idx + 1) % len(self.colors)
                elif choice == "4":
                    break
                else:
                    error_msg = "Entry invalid. Try 1, 2, 3 or 4"

            except (KeyboardInterrupt, EOFError):
                break


def main() -> None:
    generator = MazeGenerator(
        rows=10,
        cols=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=None,
        output_file="out_maze.txt"
    )

    generator.generate()

    generator.write_file()

    render = MazeRender(generator)
    render.render()
    render.interaction()


if __name__ == "__main__":
    main()
>>>>>>> f637046 (render ok):cell.py
