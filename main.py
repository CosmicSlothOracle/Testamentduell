import pygame
import sys
from game.game import TestamentDuelGame

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Testament Duel")
    
    # Set up the clock
    clock = pygame.time.Clock()
    
    # Create game instance
    game = TestamentDuelGame(screen, clock)
    
    # Run the game
    game.run()

if __name__ == "__main__":
    main()