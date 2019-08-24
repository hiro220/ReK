import pygame
from pygame.locals import *
from define import WIDTH, HEIGHT
from textbox import TextBox

class PopupWindow:

    def __init__(self, screen, text="", buttons=[]):
        self.screen = screen
        self.text = text
        self.buttons = buttons
        self.button_id = 0
        self.button_size = len(buttons) or 1
        x, y = WIDTH // 2 - 230, HEIGHT // 2 - 140
        self.textbox = TextBox(screen, x, y, 460, 200, text, outline_color=(255,255,255), font_size=25)
        self.clock = pygame.time.Clock()

    def loop(self):
        while True:
            self.clock.tick(30)
            request = self.process()
            self.draw()
            if request != None:
                return self.button_id

    def draw(self):
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        box = Rect(center_x-250, center_y-150, 500, 300)
        pygame.draw.rect(self.screen, (255,255,255), box)
        pygame.draw.rect(self.screen, (150,150,150), box, 5)
        self.textbox.draw()
        pygame.display.update()

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