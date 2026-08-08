# aqui criar  os modulos para ser importado
#  conteduo do modulo.py 6 e 9

from parser.config_parser import ConfigParser
from generator.maze_generator import MazeGenerator
from renderer.maze_renderer import MazeRenderer


def main():

    # Ler e validar o arquivo de configuração
    parser = ConfigParser("config.txt")
    config = parser.parse()

    #  Criar o gerador
    generator = MazeGenerator(config)

    # Gerar o labirinto
    maze = generator.generate()

    #  Salvar o labirinto em arquivo (.txt)
    MazeRenderer.export(maze, "maze.txt")

    # Exibir o labirinto
    renderer = MazeRenderer(maze)
    renderer.render()

    # Interação com o usuário
    renderer.interaction()

 
if __name__ == "__main__":
    main()
