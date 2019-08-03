import pygame
import sys
from pygame.locals import *
from define import EXIT

class Help_print():
    def __init__(self, screen, select_num):
        self.screen = screen
        self.back_num = 0
        self.select_num = select_num 
        self.player_image = pygame.image.load("img/player.png").convert_alpha()
        
        pygame.font.init()
        player_font = pygame.font.Font("freesansbold.ttf", 25)
        back_font = pygame.font.Font("freesansbold.ttf", 55)
        self.player_text = player_font.render("player", True, (255,255,255))
        self.back_text = back_font.render("Back", True, (255,255,255))

    
    def draw(self):

        while True:
            self.screen.blit(self.player_text, [430, 300]) 
            self.screen.blit(self.player_image, (200, 200))
            self.screen.blit(self.back_text,[800, 5])

            if self.back_num == 1:
                pygame.draw.rect(self.screen,(255,255,0),Rect(790,3,155,60),5)

            pygame.display.update()    

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.Key_Event(event)
                    if event.key == K_RETURN:
                        if self.back_num == 1:
                            return "0"
                    if event.type == QUIT:  
                        return EXIT

            self.screen.fill((0,0,0))

    def Key_Event(self, event):   
        if event.key == K_UP:
            self.back_num = 1     
       
        