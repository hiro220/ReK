#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *

class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/beam1.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines  