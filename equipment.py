import pygame
from pygame.locals import *
from define import *

class equipment:

    def __init__(self, data):
        self.data = data
    
    def do(self):
        while True:
            request = self.process()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        pass

    def draw(self):
        pass