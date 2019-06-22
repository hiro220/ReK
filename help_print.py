import pygame
import sys
from pygame.locals import *

class Help_print():
    def __init__(self, screen, select_num):
        self.screen = screen
        self.select_num = select_num 
        self.player_image = pygame.image.load("img/player.png").convert_alpha()
        
        pygame.font.init()
        print_font = pygame.font.Font("freesansbold.ttf", 25)
        self.player_text = print_font.render("player", True, (255,255,255))


    
    def draw(self):

        while True:
            self.screen.blit(self.player_text, [430, 300]) 
            self.screen.blit(self.player_image, (200, 200))

            pygame.display.update()    

            for event in pygame.event.get():
                if event.type == QUIT:         
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0,0,0))       
