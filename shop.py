#!/usr/bin/env python
# coding:utf-8

import pygame
import sys
from pygame.locals import *
from money import *

class Shop:
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data

        self.gun_num = 1
        self.back_num = 0

        self.gun_value = [1000, 1000, 1000, 1000, 1000, 1000]

        back_font = pygame.font.Font("freesansbold.ttf", 55)
        self.back_text = back_font.render("Back", True, (255, 255, 255))

    def draw(self):
        
        while True:
            for i in range(1, 7):
                gun_id = i
                gun = self.data['gun_data'][gun_id]
                gun_text = gun['name']

                if gun['own'] == 0:
                    color = (255, 255, 255)
                else:
                    color = (150, 150, 150)
                    
                draw_text = pygame.font.Font("freesansbold.ttf", 45).render(gun_text, True, color)
                self.screen.blit(draw_text, [210, 50 * i + 110])

                gun_value_text = str(self.gun_value[i - 1])
                gun_value_font = pygame.font.Font("freesansbold.ttf", 45).render(gun_value_text, True, (255, 255, 255))
                self.screen.blit(gun_value_font, [700, 50 * i + 110])

                if self.gun_num == gun_id:
                    width = draw_text.get_rect().right
                    height = draw_text.get_rect().bottom
                    pygame.draw.rect(self.screen,(255,255,0),Rect(205, 105 + i * 50, width+10, height+10),5)

            self.screen.blit(self.back_text, [900, 5])
            
            own_money = pygame.font.SysFont(None, 55).render("MONEY:" + str(self.data['money']), True, (255, 255, 255))
            self.screen.blit(own_money, (10, 10))
            
            if self.back_num == 1:
                pygame.draw.rect(self.screen,(255,255,0),Rect(890,3,150,60),5)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.Key_Event(event)
                    if event.key == K_RETURN:
                        if self.back_num == 1:
                            return "0"
                        else:
                            self.Buy()

            self.screen.fill((0,0,0))

    def Key_Event(self, event):
        if event.key == K_DOWN:
            if self.back_num == 1:
                self.back_num = 0
                self.gun_num = 1
            else:
                if self.gun_num >= 1 and self.gun_num < 6:
                    self.gun_num += 1
        elif event.key == K_UP:
            if self.gun_num == 1:
                self.back_num = 1
                self.gun_num = 0
            else:
                if self.gun_num > 1 and self.gun_num <= 6:
                    self.gun_num -= 1


    def Buy(self):
        data = self.data['gun_data']
        if data[self.gun_num]['own'] == 0:
            if self.data['money'] >= self.gun_value[self.gun_num - 1]:
                self.data['money'] -= self.gun_value[self.gun_num - 1]
                data[self.gun_num]['own'] = 1