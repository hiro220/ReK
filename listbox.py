import pygame
from pygame.locals import *
import numpy

class ListBox:

    def __init__(self, screen, x, y, width, height, data_list=[], bg=(255,255,255), outline=3, target=False, font_size=20):
        self.screen = screen
        self.rect = Rect(x, y, x+width, y+height)
        self.list = data_list
        self.bg = bg
        self.outline = outline
        self.target = target
        self.selected = 0
        self.top_id = 0
        self.font = pygame.font.Font("freesansbold.ttf", size=font_size)
        self.draw_num = height // (font_size+10)
        self.font_size = font_size

    def draw(self):
        pygame.draw.rect(self.screen, self.bg, self.rect)
        pygame.draw.rect(self.screen, (0,0,0), self.rect, self.outline)
        text_list = self.list[self.top_id:self.top_id+self.draw_num]
        x, y = self.rect.left, self.rect.top
        for i, text in enumerate(text_list):
            color = (0,0,0)
            draw_text = self.font.render(text, True, color)
            self.screen.blit(draw_text, [x+5, y+(self.font_size+10)*i])

    def process(self):
        # このListBoxがターゲットされていないなら処理はなし
        if not self.target:
            return

    def get_list(self):
        return self.list

    def set_selectable(self, selectable_list):
        pass

    def __add__(self, others_list):
        self.list += others_list