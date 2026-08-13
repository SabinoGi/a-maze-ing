                        Python Module MAZEGENERATOR Manual

NAME
     MazeGenerator - Lead orchestrator for maze generation, validation, and export.

SYNOPSIS
     class MazeGenerator:
         def __init__(
             self,
             rows: int,
             cols: int,
             entry: tuple[int, int],
             exit: tuple[int, int],
             perfect: bool,
             seed: int | None = None,
             output_file: str = "maze.txt"
         ) -> None

         def generate(self) -> None
         def get_maze_data(self) -> tuple[list[list[int]], list[str]]
         def write_file(self) -> None


DESCRIPTION
     The MazeGenerator module is the main component responsible for building 
     the grid, executing carving algorithms, writing data to disk, and extracting 
     maze solution structures.

CONFIGURATION PARAMETERS
     rows         Total number of rows in the maze.
     cols         Total number of columns in the maze.
     entry        Cartesian coordinate (X, Y) x is the column and y is the row.
     exit         Cartesian coordinate (X, Y) x is the column and y is the row.
     perfect      Boolean flag. True generates a perfect maze (no loops, single path).
                  False introduces loops and redundant paths.
     seed         PRNG seed. If set to None, generation will be non-deterministic.
     output_file  Path to the output text file. Default: "maze.txt".

BITWISE WALL MAPPING (IntFlag)
     The internal binary representation of wall states per cell follows this layout:

     FLAGS       BINARY MASK       DECIMAL   HEXADECIMAL
     --------------------------------------------------
     NORTH       0b0001            1         0x1
     EAST        0b0010            2         0x2
     SOUTH       0b0100            4         0x4
     WEST        0b1000            8         0x8

FILE OUTPUT FORMAT (output_file)
     The file created by the write_file() method contains the cell grid map 
     encoded in Hexadecimal format (0-F) representing the combined wall bitmask, 
     followed by the navigational solution sequence (N, S, E, W).

USAGE EXAMPLE
    $ cat example.py

    from mazegen import MazeGenerator

        def main() -> None:

            generator = MazeGenerator(
                rows=10,
                cols=10,
                entry=(0, 0),
                exit=(9, 9),
                perfect=True,
                seed=42,
                output_file="maze.txt",
            )

            generator.generate()
            generator.write_file()

            matrix_status, solution_path = generator.get_maze_data()

            print(f"Cell (0,0) Mask: {matrix_status[0][0]}")
            print(f"Solution [N,S,E,W]: {solution_path}")

        if __name__ == "__main__":
            main()

EXECUTION OUTPUT
     $ python3 example.py
     Cell (0,0) Mask: 9
     Solution [N,S,E,W]: ['E', 'E', 'S', 'S', 'E', 'S', 'W', 'S', 'E', 'S']

     $ cat out_maze.txt
     9A3C...
     EESSESWSES
