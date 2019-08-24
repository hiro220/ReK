import pygame
from pygame.locals import *
from define import WIDTH, HEIGHT
from textbox import TextBox

class PopupWindow:

    def __init__(self, screen, text="", buttons=[]):
        self.screen = screen
        self.text = text
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        self.rect = Rect(center_x-250, center_y-150, 500, 300)
        x, y = WIDTH // 2 - 230, HEIGHT // 2 - 140
        self.textbox = TextBox(screen, x, y, 460, 200, text, outline_color=(255,255,255), \
                               font_size=25, align=('center', 'center'))
        self.buttons = []
        self.button_id = 0
        self.button_size = len(buttons) or 1
        frame = 500 / self.button_size
        x = self.rect.left + frame/2 - 50
        y = self.rect.bottom - 80
        for button in buttons:
            button = TextBox(screen, x, y, 100, 50, button, outline_color=(255,255,255), align=('center', 'center'))
            x += frame
            self.buttons.append(button)
        self.clock = pygame.time.Clock()

    def loop(self):
        while True:
            self.clock.tick(30)
            request = self.process()
            self.draw()
            if request != None:
                return self.button_id

    def draw(self):
        # ウィンドウを塗りつぶす
        pygame.draw.rect(self.screen, (255,255,255), self.rect)
        # ウィンドウの枠を描画
        pygame.draw.rect(self.screen, (150,150,150), self.rect, 5)
        # テキストを描画
        self.textbox.draw()
        # ボタン情報を描画
        for i, button in enumerate(self.buttons):
            # ボタンのテキストを描画
            button.draw()
            # ボタンの枠を描画
            color = (255, 0, 0) * (i==self.button_id) or (0,)*3
            outline = 2 + (i==self.button_id)
            pygame.draw.rect(self.screen, color, button.rect, outline)
        pygame.display.update()

    def process(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.button_id += 1
                elif event.key == K_LEFT:
                    self.button_id -= 1
                elif event.key == K_RETURN:
                    return self.button_id
                self.button_id = (self.button_id + self.button_size) % self.button_size
        return None