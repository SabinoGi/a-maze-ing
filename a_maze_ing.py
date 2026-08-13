from mazegen import MazeGenerator
from render import MazeRender
from 

def main():

    parser = ConfigParser("config.txt")
    config = parser.parse()

    generator = MazeGenerator(config)
    generator.generate()

    generator.write_file()

    render = MazeRender(generator)
    render.render()
    render.interaction()
 

if __name__ == "__main__":
    main()
