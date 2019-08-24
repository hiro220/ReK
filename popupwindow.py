import pygame
from pygame.locals import *
from define import WIDTH, HEIGHT
from textbox import TextBox

class PopupWindow:

    def __init__(self, screen, text="", buttons=[], target=0, title=""):
        self.screen = screen
        self.outline_color = (50, 50, 50)
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        self.rect = Rect(center_x-250, center_y-150, 500, 300)
        self.title = None
        if title != "":
            self.title = TextBox(screen, self.rect.left, self.rect.top, 500, 32, title, \
                                 font_size=25, outline_color=self.outline_color, outline_size=5)
        x, y = WIDTH // 2 - 230, HEIGHT // 2 - 100
        self.textbox = TextBox(screen, x, y, 460, 155, text, outline_color=(255,)*3, \
                               font_size=25, align=('center', 'center'))
        self.buttons = []
        self.button_id = target
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
        if self.title != None:
            self.title.draw()
        # ウィンドウの枠を描画
        pygame.draw.rect(self.screen, self.outline_color, self.rect, 5)
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