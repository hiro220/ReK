# coding:utf-8

from machine import Machine
import pygame
from pygame.locals import *
from gun import *
from define import INFO_WIDTH, WIDTH, HEIGHT

class PlayerMachine(Machine):
    killed_count = 0
    def __init__(self, x, y, cpus, score, money):
        """引数は、初期位置(x, y)、弾の当たり判定対象となる敵機グループ"""
        image = pygame.image.load("img/player.png").convert_alpha()
        super().__init__(2, x, y, image, cpus, score, money)
        self.dx, self.dy = 7, 7                         # 移動量
        self.set = 0
        self.cop_flag = True
        self.gun = Missile_Gun(self.machines, self, 100)

    def move(self):
        key = pygame.key.get_pressed()      # 押されたキーを受け取る
        if key[K_UP]:                       # 矢印キー上が押されているとき(長押し)
            super().move(0, -self.dy)
        if key[K_DOWN]:                     # 矢印キー下が押されているとき(長押し)
            super().move(0, self.dy)
        if key[K_RIGHT]:                    # 矢印キー右が押されているとき(長押し)
            super().move(self.dx, 0)
        if key[K_LEFT]:                     # 矢印キー左が押されているとき(長押し)
            super().move(-self.dx, 0)
        self.rect.clamp_ip(Rect(INFO_WIDTH, 0, WIDTH, HEIGHT))       # 画面外に出たとき、画面内に収まるよう移動

    def shoot(self, key):
        if key == K_x:              # ｘキーが押されたとき弾を発射
            x, y = self.rect.midright
            super().shoot(x, y)
        elif key == K_v:
            super().reload()

    def change(self, key):
        if key == K_a:
            self.gun = Circle_Gun(self.machines, self, 10)   
        elif key == K_s:
            self.gun = Reflection_Gun(self.machines, self, 10)
        elif key == K_d:
            super().change(2)
    
    def isGameOver(self):
        return not self.alive()

    def death(self):
        PlayerMachine.killed_count += 1