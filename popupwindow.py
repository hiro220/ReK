import pygame
from pygame.locals import *

class PopupWindow:

    def __init__(self, screen, text="", buttons=[]):
        self.screen = screen
        self.text = text
        self.buttons = buttons
        self.clock = pygame.time.Clock()

    def loop(self):
        while True:
            self.clock.tick(30)
            button_id = self.process()
            self.draw()
            if button_id != None:
                return button_id

    def draw(self):
        pass

    def process(self):
        pass