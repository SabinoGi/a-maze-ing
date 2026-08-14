import sys
from mazegen import MazeGenerator
from render import MazeRender
from config_parser import ConfigParser, ConfigError


def parse_args() -> str:
    """Garante que o caminho do arquivo foi passado no terminal."""
    if len(sys.argv) != 2:
        print("Error: Use: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
    return sys.argv[1]


def main() -> int:
    try:
        config_file = parse_args()
        parser = ConfigParser(config_file)
        config = parser.parse()
    except (ValueError, FileNotFoundError, ConfigError) as error:
        print(F"Error: {error}")
        return 1

    generator = MazeGenerator(
        rows=config["HEIGHT"],
        cols=config["WIDTH"],
        entry=config["ENTRY"],
        exit=config["EXIT"],
        perfect=config["PERFECT"],
        output_file=config["OUTPUT_FILE"],
        seed=config["SEED"]
    )

    generator.generate()
    generator.write_file()

    render = MazeRender(generator)
    render.render()
    render.interaction()
    return 0


if __name__ == "__main__":
    sys.exit(main())
