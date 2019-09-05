from boss import Boss
import pygame
from define import *
from item import *
from gun import *
from timer import Timer

img_path = "img/cpu/"

class Stage4_Boss(Boss):

    def __init__(self, x, y, players, score, money):
        image = pygame.image.load(img_path+"cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10, x, 300, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.dx, self.dy = -2, 0

    def update(self):
        if self.rect.centerx <= 1000:
            self.dx = 0
        self.move(self.dx, self.dy)

    def create_item(self):
        pass
