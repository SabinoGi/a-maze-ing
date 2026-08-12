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


=======
    #  Criar o gerador e gerar o labirnto
    generator = MazeGenerator(config).generate()

    generator_maze = generator.get_walls_grid()

    #  Salvar o labirinto em arquivo (.txt)
    MazeRenderer.export(generator_maze, "maze.txt")

    # Exibir o labirinto
    renderer = MazeRenderer(generator.grid).render()

    # Interação com o usuário
    renderer.interaction()

 
>>>>>>> ce88bdf (render loadinhg)
if __name__ == "__main__":
    main()
