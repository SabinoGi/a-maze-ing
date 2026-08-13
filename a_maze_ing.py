import sys
from mazegen import MazeGenerator
from render import MazeRender
from config_parser import ConfigParser


def parse_args() -> str:
    """Garante que o caminho do arquivo foi passado no terminal."""
    if len(sys.argv) != 2:
        print("Error: Use: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
    return sys.argv[1]


# def run_tests(config: dict[str, Any]) -> None:
#     """Isola as impressões de teste e inspeção de dados."""
#     print("--- [ TESTE DE CONFIGURAÇÃO ] ---")
#     print(f"Tipo do objeto: {type(config)}")
#     print(f"Conteúdo: {config}")
#     print("---------------------------------")


def main() -> None:
    config_file = parse_args()

    parser = ConfigParser(config_file)
    config = parser.parse()

    seed_val = int(config["SEED"]) if config.get("SEED") is not None else None

    generator = MazeGenerator(
        rows=config["HEIGHT"],
        cols=config["WIDTH"],
        entry=config["ENTRY"],
        exit=config["EXIT"],
        perfect=config["PERFECT"],
        output_file=config["OUTPUT_FILE"],
        seed=seed_val,
    )

    generator.generate()
    generator.write_file()

    render = MazeRender(generator)
    render.render()
    render.interaction()


if __name__ == "__main__":
    main()
