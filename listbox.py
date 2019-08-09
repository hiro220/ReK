import pygame
from pygame.locals import *
from define import EXIT
import numpy

class ListBox:

    def __init__(self, screen, x, y, width, height, data_list=[], bg=(255,255,255), outline=3, target=False, font_size=20):
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.list = data_list
        self.bg = bg
        self.outline = outline
        self.target = target
        self.selected = 0
        self.top_id = 0
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.draw_num = height // (font_size+10)
        self.font_size = font_size
        self.list_size = len(self.list)

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
        for event in pygame.event.get():
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.selected -= 1
                elif event.key == K_DOWN:
                    self.selected += 1
                elif event.key == K_RETURN:
                    self.target = False
                    return self.selected
                else:
                    self.target = False
                self.selected = (self.selected+self.list_size) % self.list_size
                self.top_id = (self.top_id <= self.selected <= self.top_id+self.draw_num-1) * self.top_id or \
                              (self.top_id+self.draw_num-1 < self.selected) * (self.selected-self.draw_num+1) or \
                              (self.top_id > self.selected) * (self.selected)

    def get_list(self):
        return self.list

    def set_selectable(self, selectable_list):
        pass

    def __call__(self):
        self.target ^= True

    def __add__(self, others_list):
        self.list += others_list