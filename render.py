from mazegen import MazeGenerator, MazeSolver, Wall


class MazeRender:
    """Renders the maze in the terminal and manages the user menu.."""

    def __init__(self, generator: MazeGenerator) -> None:
        self.generator = generator
        self.show_path = False
        self.colors = [
            "\033[97m", "\033[94m", "\033[92m", "\033[93m", "\033[96m"]
        self.color_idx = 0

    def render(self) -> None:
        grid = self.generator.grid
        wall_color = self.colors[self.color_idx]

        """Element styles"""
        QUINA = f"\033[1m{wall_color}■\033[0m"
        TETO = f"\033[1m{wall_color}━━━\033[0m"
        PAREDE = f"\033[1m{wall_color}┃\033[0m"
        VAZIO = "   "

        """Special fills"""
        ENTRY_BG = "\033[45m   \033[0m"    # Rosa/Magenta
        EXIT_BG = "\033[41m   \033[0m"     # Vermelho
        PATH_BG = "\033[44m   \033[0m"     # Verde
        PATTERN_BG = "\033[47m   \033[0m"  # Cinza ('42')

        """Obtains the solution steps only if the option is enabled."""
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

        """Maze design"""
        for row in range(grid.rows):
            """Top line"""
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                top = TETO if cell.has_wall(Wall.NORTH) else VAZIO
                print(f"{QUINA}{top}", end="")
            print(QUINA)

            """Core content and side walls"""
            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                left = PAREDE if cell.has_wall(Wall.WEST) else " "

                """Sets the cell background color"""
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

            """East wall of the last column"""
            last_cell = grid.get_cell(row, grid.cols - 1)
            right = PAREDE if last_cell.has_wall(Wall.EAST) else " "
            print(right)

        """Bottom line of the last row"""
        for col in range(grid.cols):
            cell = grid.get_cell(grid.rows - 1, col)
            bottom = TETO if cell.has_wall(Wall.SOUTH) else VAZIO
            print(f"{QUINA}{bottom}", end="")
        print(QUINA)

    def interaction(self) -> None:
        """Displays the menu without external modules."""
        error_msg = ""

        while True:
            """Clears the terminal and renders the current maze."""
            print("\033[H\033[2J", end="")
            self.render()

            """If there was a previous typing error, it is displayed now."""
            if error_msg:
                print(f"\n\033[91m{error_msg}\033[0m")
                error_msg = ""

            """Displays the menu"""
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show / Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")

            try:
                choice = input("\033[92mChoice? (1-4): \033[0m").strip()

                if choice == "1":
                    self.generator.generate()
                    self.generator.write_file()
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
        output_file=""
    )

    generator.generate()

    generator.write_file()

    render = MazeRender(generator)
    render.render()
    render.interaction()


if __name__ == "__main__":
    main()
