import pygame
import sys
from pygame.locals import *

class Help_a: 
    def __init__(self, screen):
        self.screen = screen
        self.count = 0
        pygame.font.init()
        explain_font = pygame.font.Font("freesansbold.ttf", 25)
        explain_font1 = pygame.font.Font("freesansbold.ttf", 25)
        with open('testa/test.txt', 'r', encoding="utf-8") as fp:   # ファイルを読み取り専用で開く
            self.dic1 = {}                     # 辞書を定義する
            self.dic2 = {}
            self.dic3 = {}
            self.dic4 = {}
            self.dic5 = {}
            self.dic6 = {}
            self.dic7 = {}
            self.dic_data = [self.dic1, self.dic2, self.dic3, self.dic4, self.dic5, self.dic6, self.dic7]
            for (line, data) in zip(fp.readlines(), self.dic_data):                 # ファイルを一行ごとに読み取り、変数lineに文字列として格納する
                if self.count == 0:
                    print(data)
                    data = line.strip('\n')       # 改行コード'\n'を取り除き、タブ区切りでリストに分割する
                    
                    self.help_text1 = explain_font.render(data, True, (255,255,255))
                    self.count += 1
                elif self.count == 1:
                    self.dic2 = line.strip('\n')
                    self.help_text2 = explain_font.render(self.dic2, True, (255,255,255))
                    self.count += 1
                elif self.count == 2:
                    self.dic3 = line.strip('\n')
                    self.help_text3 = explain_font1.render(self.dic3, True, (255,255,255))
                    self.count += 1
                elif self.count == 3:
                    self.dic4 = line.strip('\n')
                    self.help_text4 = explain_font.render(self.dic4, True, (255,255,255))
                    self.count += 1
                elif self.count == 4:
                    self.dic5 = line.strip('\n')
                    self.help_text5 = explain_font.render(self.dic5, True, (255,255,255))
                    self.count += 1
                elif self.count == 5:
                    self.dic6 = line.strip('\n')
                    self.help_text6 = explain_font.render(self.dic6, True, (255,255,255))
                    self.count += 1
                elif self.count == 6:
                    self.dic7 = line.strip('\n')
                    self.help_text7 = explain_font.render(self.dic7, True, (255,255,255))
                    self.count += 1
        
    def draw(self):
        
        while True:
            self.screen.blit(self.help_text1, [430, 20]) 
            self.screen.blit(self.help_text2, [0, 30]) 
            self.screen.blit(self.help_text3, [430, 60]) 
            self.screen.blit(self.help_text4, [430, 80]) 
            self.screen.blit(self.help_text5, [430, 100]) 
            self.screen.blit(self.help_text6, [430, 120]) 
            self.screen.blit(self.help_text7, [430, 140]) 
            pygame.display.update()
            #self.count += 10

            for event in pygame.event.get():   
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill((0,0,0))