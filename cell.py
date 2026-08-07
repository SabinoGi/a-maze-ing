from enum import IntFlag


class Wall(IntFlag):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

# utiliza composição: tem uma
class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False

        self.walls = (
            Wall.NORTH |
            Wall.EAST |
            Wall.SOUTH |
            Wall.WEST
        )

# o maze cria a base 
# grid == dados bidimensionnal
class Maze():
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.grid = []

        for row in range(rows):
            line = []

            for col in range(cols):
                line.append(Cell(row, col))

            self.grid.append(line)


def main():
    maze = Maze(4, 2)

    for row in maze.grid:
        for cell in row:
            print(
                f"({cell.row},{cell.col}) "
                f"{cell.walls:X}",
                end="   "
            )
        print()


if __name__ == "__main__":
    main()
