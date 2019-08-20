import pygame
from pygame.locals import *

class PopupWindow:

    def __init__(self, screen, text="", buttons=[]):
        self.screen = screen
        self.text = text
        self.buttons = buttons
        self.button_id = 0
        self.button_size = len(buttons) or 1
        self.clock = pygame.time.Clock()

    def loop(self):
        while True:
            self.clock.tick(30)
            request = self.process()
            self.draw()
            if request != None:
                return self.button_id

    def draw(self):
        pass

    def process(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.button_id += 1
                elif event.key == K_LEFT:
                    self.button_id -= 1
                elif event.key == K_RETURN:
                    return 1
                self.button_id = (self.button_id + self.button_size) % self.button_size
        return None