#!/usr/bin/env python
# coding:utf:-8

import pygame
from pygame.locals import *
from gun import Gun

class Machine(pygame.sprite.Sprite):

    def __init__(self, hp, x, y, img, machines):
        """引数は、機体の体力を表すhp、機体の初期位置(x, y)、描画する画像、発射する弾の当たり判定対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.hp = hp
        self.image = img            # 引数の画像をインスタンス変数に保存する
        self.rect = img.get_rect()  # 画像からrectを取得する
        self.rect.move_ip(x, y)             # 初期位置に移動させる
        self.gun = Gun(machines)    # Gunクラスのインスタンスを生成する

    def move(self, dx, dy):
        # 引数に指定しただけ移動する
        self.rect.move_ip(dx, dy)

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        if not self.gun.isBulletZero():     # 残弾数が0でないなら弾を発射する
            self.gun.shoot(x, y)