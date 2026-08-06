from enum import IntFlag

# class corenadas de uma celula
class Wall(IntFlag):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

# clss cell: cada celula tem posiçaõ linha e coluna 
# e se foi visitada e as paredes  
class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
# aqui aconetce a junçaõ de todas "|" as cordenadas ligadas
        self.walls = (
            Wall.NORTH |
            Wall.EAST |
            Wall.SOUTH |
            Wall.WEST
        )

# o maze cria a a base 
class Maze(Cell):
    def __init__(self, rows: int, cols: int):
        super().__init__(row, col)
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
