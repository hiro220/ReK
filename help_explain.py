import pygame
import sys
from pygame.locals import *

class Help_a: 
    def __init__(self, screen):
        self.screen = screen
        self.count = 0
        pygame.font.init()
        explain_font = pygame.font.Font("freesansbold.ttf", 25)
        with open('testa/test.txt', 'r', encoding="utf-8") as fp:   # ファイルを読み取り専用で開く
            self.dic_data = [0, 1, 2, 3, 4, 5, 6]
            for (line, data) in zip(fp.readlines(), range(len(self.dic_data))):                 # ファイルを一行ごとに読み取り、変数lineに文字列として格納する
                self.dic_data[data] = line.strip('\n')       # 改行コード'\n'を取り除き、タブ区切りでリストに分割する
                self.dic_data[data] = explain_font.render(self.dic_data[data], True, (255,255,255))
                
        
    def draw(self):
        
        while True:
            self.screen.blit(self.dic_data[0], [430, 20]) 
            self.screen.blit(self.dic_data[1], [0, 30]) 
            self.screen.blit(self.dic_data[2], [430, 60]) 
            self.screen.blit(self.dic_data[3], [430, 80]) 
            self.screen.blit(self.dic_data[4], [430, 100]) 
            self.screen.blit(self.dic_data[5], [430, 120]) 
            self.screen.blit(self.dic_data[6], [430, 140]) 
            pygame.display.update()
            #self.count += 10

            for event in pygame.event.get():   
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill((0,0,0))