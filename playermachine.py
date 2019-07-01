# coding:utf-8

from machine import Machine
import pygame
from pygame.locals import *
from gun import *

class PlayerMachine(Machine):

    def __init__(self, x, y, cpus, score):
        """引数は、初期位置(x, y)、弾の当たり判定対象となる敵機グループ"""
        image = pygame.image.load("img/player.png").convert_alpha()
        super().__init__(2, x, y, image, cpus, score)
        self.dx, self.dy = 7, 7                         # 移動量
        self.cop_flag = True
        self.gun = Beam_Gun(self.machines, self, 100)

    def move(self, height, width):
        key = pygame.key.get_pressed()      # 押されたキーを受け取る
        if key[K_UP]:                       # 矢印キー上が押されているとき(長押し)
            super().move(0, -self.dy)
        if key[K_DOWN]:                     # 矢印キー下が押されているとき(長押し)
            super().move(0, self.dy)
        if key[K_RIGHT]:                    # 矢印キー右が押されているとき(長押し)
            super().move(self.dx, 0)
        if key[K_LEFT]:                     # 矢印キー左が押されているとき(長押し)
            super().move(-self.dx, 0)
        self.rect.clamp_ip(Rect(0, 0, width, height))       # 画面外に出たとき、画面内に収まるよう移動

    def shoot(self, key):
        if key == K_x:              # ｘキーが押されたとき弾を発射
            x, y = self.rect.midright
            super().shoot(x, y)
        elif key == K_v:
            super().reload()
    
    def isGameOver(self):
        return not self.alive()