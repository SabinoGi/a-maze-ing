import random
from .maze import Grid, Cell, Wall


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


class MazePacMan:
    def __init__(self, grid: Grid, rng: random.Random) -> None:
        self.grid = grid
        self.rng = rng

    def _is_dead_end(self) -> list[Cell]:
        """Identifies cells with 3 or 4 closed
        walls that are NOT part of the '42' pattern."""
        dead_ends: list[Cell] = []

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.get_cell(r, c)

                if cell.is_42:
                    continue

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
