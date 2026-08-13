from .maze import Grid, Wall


class MazeRenderer:
    def __init__(self, grid: Grid):
        self.grid = grid

    def show(self) -> None:
        for row in range(self.grid.rows):
            # Linha superior
            for col in range(self.grid.cols):
                cell = self.grid.get_cell(row, col)

                if cell.walls & Wall.NORTH:
                    print("+---", end="")
                else:
                    print("+   ", end="")

            print("+")

            # Conteúdo + paredes laterais
            for col in range(self.grid.cols):
                cell = self.grid.get_cell(row, col)

                if cell.walls & Wall.WEST:
                    print("|", end="")
                else:
                    print(" ", end="")

                if cell.is_42:
                    print("\033[41m   \033[0m", end="")
                else:
                    print("   ", end="")

            # Parede direita
            cell = self.grid.get_cell(row, self.grid.cols - 1)

            if cell.walls & Wall.EAST:
                print("|")
            else:
                print(" ")

        # Linha inferior
        for col in range(self.grid.cols):
            cell = self.grid.get_cell(self.grid.rows - 1, col)

            if cell.walls & Wall.SOUTH:
                print("+---", end="")
            else:
                print("+   ", end="")

        print("+")

    def export(self, file_name: str) -> None:
        try:
            with open(file_name, "w") as file:
                for row in range(self.grid.rows):
                    for col in range(self.grid.cols):
                        cell = self.grid.get_cell(row, col)
                        file.write(f"{cell:x}")

        except PermissionError as error:
            print(f"Error writing file '{file_name}': {error}")