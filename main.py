from src.maze import MazeGenerator
from src.renderer import MazeRenderer


def main():
    generator = MazeGenerator(
        rows=20,
        cols=20,
        entry=(1, 1),
        exit=(19, 14),
        perfect=True,
        seed=42,
        output_file="out_maze.txt"
    )

    generator.generate()


    renderer = MazeRenderer(generator.grid)
    renderer.show()
    renderer.export("out_maze.txt")



    #  Criar o gerador e gerar o labirnto
    generator = MazeGenerator(config).generate()

    #  Salvar o labirinto em arquivo (.txt)
    generator.write_file()

    # Exibir o labirinto
    MazeRenderer(generator.grid).render()

    # Interação com o usuário
    #MazeRenderer(generator.grid).interaction()

 

if __name__ == "__main__":
    main()
