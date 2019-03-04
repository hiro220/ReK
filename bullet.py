#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/bullet1.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 当たりを判定する機体のグループ
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。

    def move(self):
        self.rect.move_ip(self.dx, self.dy)     # 弾を移動させる
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)

class Reflection_Bullet(Bullet):
    def __init__(self, x, y, dx, dy, machines):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/bullet1.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines
        self.count = 0

        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。

    def move(self):
        self.rect.move_ip(self.dx, self.dy)
        if self.rect.bottom >= 600 or self.rect.top <= 0 and self.count <= 5:
            self.dy *= -1
            self.count += 1
        elif self.rect.right >= 960 or self.rect.left <= 0 and self.count <= 5:
            self.dx *= -1
            self.count += 1
        
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)