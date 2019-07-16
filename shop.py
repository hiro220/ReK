#!/usr/bin/env python
# coding:utf-8

import pygame
import sys
from pygame.locals import *
from money import *

class Shop:
    def __init__(self, screen):
        self.screen = screen

        self.gun_num = 1
        self.back_num = 0

        Circle_gun_font = pygame.font.Font("freesansbold.ttf", 45)
        Circle_gun_place_font = pygame.font.Font("freesansbold.ttf", 45)
        Reflection_Gun_font = pygame.font.Font("freesansbold.ttf", 45)
        Reflection_Gun_place_font = pygame.font.Font("freesansbold.ttf", 45)

        back_font = pygame.font.Font("freesansbold.ttf", 55)

        self.Circle_gun_text = Circle_gun_font.render("Circle_Gun", True, (255, 255, 255))
        self.Circle_gun_place_text = Circle_gun_place_font.render("1000", True, (255, 255, 255))
        self.Reflection_Gun_text = Reflection_Gun_font.render("Reflection_Gun", True, (255, 255, 255))
        self.Reflection_Gun_place_text = Reflection_Gun_place_font.render("1500", True, (255, 255, 255))
        self.back_text = back_font.render("Back", True, (255, 255, 255))

    def draw(self):
        while True:
            self.screen.blit(self.Circle_gun_text, [210, 150])
            self.screen.blit(self.Circle_gun_place_text, [700, 150])
            self.screen.blit(self.Reflection_Gun_text, [210, 250])
            self.screen.blit(self.Reflection_Gun_place_text, [700, 250])
            self.screen.blit(self.back_text, [900, 5])

            if self.gun_num == 1:
                pygame.draw.rect(self.screen,(255,255,0),Rect(210,150,250,60),5)
            elif self.gun_num == 2:
                pygame.draw.rect(self.screen,(255,255,0),Rect(210,250,350,60),5)
            
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
                            return self.gun_num

            self.screen.fill((0,0,0))

    def Key_Event(self, event):
        if event.key == K_DOWN:
            if self.back_num == 1:
                self.back_num = 0
                self.gun_num = 1
            else:
                if self.gun_num >= 1 and self.gun_num < 2:
                    self.gun_num += 1
        elif event.key == K_UP:
            if self.gun_num == 1:
                self.back_num = 1
                self.gun_num = 0
            else:
                if self.gun_num > 1 and self.gun_num <= 2:
                    self.gun_num -= 1
