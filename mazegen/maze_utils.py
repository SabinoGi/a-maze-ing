from maze import Grid, Wall, Cell
from collections import deque


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
