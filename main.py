import pygame
import sys
from constants import WIDTH, HEIGHT
from menu import MenuScreen
from game import Game


def main():
    pygame.init()
    pygame.display.set_caption("Jumper")
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    config = MenuScreen(surface).run()
    game = Game(surface, config)

    while True:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update(keys)
        game.draw()
        pygame.display.flip()
        clock.tick(game.config['fps'])


if __name__ == "__main__":
    main()
