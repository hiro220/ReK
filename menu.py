import pygame
from pygame.locals import *
import sys
import time

class Menu:
    
    def __init__(self, screen):
        self.screen = screen
        self.stage_num = 1
        self.select_num = 0

        StageSelect_font = pygame.font.Font("freesansbold.ttf", 55)
        LeftArrow_font = pygame.font.Font("freesansbold.ttf", 150)
        RightArrow_font = pygame.font.Font("freesansbold.ttf", 150)
        Stage1_font = pygame.font.Font("freesansbold.ttf", 45)
        Stage2_font = pygame.font.Font("freesansbold.ttf", 45)
        Stage3_font = pygame.font.Font("freesansbold.ttf", 45)


        self.StageSelect_text = StageSelect_font.render("Stage Select", True, (255,255,255)) 
        self.RightArrow_text = RightArrow_font.render(">", True, (255,255,255))
        self.LeftArrow_text = LeftArrow_font.render("<", True, (255,255,255))
        self.Stage1_text = Stage1_font.render("Stage1", True, (255,255,255))
        self.Stage2_text = Stage2_font.render("Stage2", True, (255,255,255))
        self.Stage3_text = Stage3_font.render("Stage3", True, (255,255,255))

    def draw(self):

        while True:
            self.screen.blit(self.StageSelect_text, [5, 5])
            self.screen.blit(self.RightArrow_text, [865, 220])
            self.screen.blit(self.LeftArrow_text, [5, 220])

            if self.stage_num == 1:
                self.screen.blit(self.Stage1_text, [110, 80])
                pygame.draw.rect(self.screen,(0,0,255),Rect(100,70,760,460),5)
            elif self.stage_num == 2:
                self.screen.blit(self.Stage2_text, [110, 80])
                pygame.draw.rect(self.screen,(0,255,0),Rect(100,70,760,460),5)
            elif self.stage_num == 3:
                self.screen.blit(self.Stage3_text, [110, 80])
                pygame.draw.rect(self.screen,(255,0,0),Rect(100,70,760,460),5)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if self.stage_num != 3:
                            self.stage_num += 1
                    elif event.key == K_LEFT:
                        if self.stage_num != 1:
                            self.stage_num -= 1
                    elif event.key == K_SPACE:
                        return self.stage_num
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            self.screen.fill((0,0,0))