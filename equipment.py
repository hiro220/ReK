import pygame
from pygame.locals import *
from define import *

class Equipment:

    def __init__(self, screen, data):
        self.data = data
        self.screen = screen
        self.selected = 0
        self.change_gun = 0
        self.guns_num = len(self.data['gun_data'])
        self.back = False
        self.screen_info = pygame.font.Font("freesansbold.ttf" ,70).render("Equip", True, (255,255,255))
        self.back_info = pygame.font.Font("freesansbold.ttf" ,50).render("'Q' : Back", True, (255,255,255))
    
    def do(self):
        while True:
            request = self.process()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        # 内部処理
        for event in pygame.event.get():
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.selected += 1
                elif event.key == K_DOWN:
                    self.selected -= 1
                elif event.key == K_RIGHT:
                    self.change_gun += 1
                elif event.key == K_LEFT:
                    self.change_gun -= 1
                elif event.key == K_q:
                    return BACK
                elif event.key == K_RETURN:
                    self.check()
                self.selected = (self.selected+self.guns_num) % self.guns_num
                self.change_gun = (self.change_gun + 3) % 3
        return CONTINUE

    def draw(self):
        # 画面描画
        self.screen.fill((0,0,0))
        self.screen.blit(self.screen_info, [150, 20])
        self.screen.blit(self.back_info, [WIDTH-self.back_info.get_rect().right-20, 20])
        pygame.display.update()

    def check(self):
        # 装備変更確認
        pass