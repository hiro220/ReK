import pygame
from pygame.locals import *
from define import *

class equipment:

    def __init__(self, data):
        self.data = data
        self.selected = 0
        self.guns_num = len(self.data['gun_data'])
    
    def do(self):
        while True:
            request = self.process()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.selected += 1
                elif event.key == K_DOWN:
                    self.selected -= 1
                self.selected = (self.selected+self.guns_num) % self.guns_num
                elif event.key == K_RETURN:
                    pass
        return CONTINUE

    def draw(self):
        pass