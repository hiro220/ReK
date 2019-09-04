#!/usr/bin/env python
# coding:utf-8

import pygame
import sys
from pygame.locals import *
from money import *
from define import *
from listbox import ListBox

class Shop:
    def __init__(self, screen, data):
        self.data = data       
        self.gun_data = self.data["gun_data"]
        self.screen = screen
        self.change_gun = 0             # 現在選択している装備場所
        self.screen_info = pygame.font.Font("freesansbold.ttf" ,70).render("Shop", True, (255,255,255))
        self.back_info = pygame.font.Font("freesansbold.ttf" ,50).render("'Q' : Back", True, (255,255,255))

        self.gun_value = [1000, 1000, 1000, 1000, 1000, 1000]

        texts = [data["name"] for data in self.gun_data.values()]
        del texts[0]
        
        self.listbox = ListBox(self.screen, 80, 150, 300, 250, texts, font_size=40, target=True)
        self.listbox.set_selectable([data["own"]==1 for data in self.gun_data.values()])

        self.clock = pygame.time.Clock()

    def do(self):
        while True:
            self.clock.tick(30)
            request = self.process()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        # 内部処理
        self.listbox()
        for event in pygame.event.get():
            select = self.listbox.process(event)
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:    
                if event.key == K_q:
                    return BACK
                self.change_gun = (self.change_gun + 3) % 3
                
        return CONTINUE

    def draw(self):
        # 画面描画
        self.screen.fill((0,0,0))
        self.screen.blit(self.screen_info, [150, 20])
        self.screen.blit(self.back_info, [WIDTH-self.back_info.get_rect().right-20, 20])
        
        self.listbox.color_reset()
        self.listbox.draw()
        pygame.display.update()

    def Buy(self):
        data = self.data['gun_data']
        if data[self.gun_num]['own'] == 0:
            if self.data['money'] >= self.gun_value[self.gun_num - 1]:
                self.data['money'] -= self.gun_value[self.gun_num - 1]
                data[self.gun_num]['own'] = 1