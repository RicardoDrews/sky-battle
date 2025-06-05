from Recursos.config import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((larguraTela, alturaTela))
        pygame.display.set_caption("Sky Battle")
        self.clock = pygame.time.Clock()


    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


if __name__ == "__main__":
    game = Game()
    game.run()