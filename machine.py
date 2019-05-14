#!/usr/bin/env python
# coding:utf:-8

import pygame
from pygame.locals import *
from gun import *

class Hp:
    def __init__(self, hp):
        self.maxhp = self.hp = hp       # 体力の上限、現在の体力に引数をセットする

    def damage(self, attack):
        """引数attack分の体力を減少させ、体力がなくなればTrueが返る"""
        self.hp -= attack
        return self.hp <= 0

    def recover(self, num):
        """引数numで指定した値だけ体力を回復する。ただし、体力の上限まで"""
        self.hp += num
        if self.hp > self.maxhp:
            self.hp = self.maxhp

class Machine(pygame.sprite.Sprite):

    def __init__(self, hp, x, y, img, machines, score):
        """引数は、機体の体力を表すhp、機体の初期位置(x, y)、描画する画像、発射する弾の当たり判定対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.hp = Hp(hp)
        self.image = img            # 引数の画像をインスタンス変数に保存する
        self.rect = img.get_rect()  # 画像からrectを取得する
        self.rect.move_ip(x, y)     # 初期位置に移動させる
        self.gun = Gun(machines, 10)    # Gunクラスのインスタンスを生成する
        self.gun2 = Tracking_Gun(machines, 10)
        self.gun3 = Opposite_Gun(machines, 10)
        self.gun4 = Reflection_Gun(machines, 10)
        self.gun5 = Circle_Gun(machines, 10)
        self.machines = machines

        self.dx = self.dy = 0
        self.score = score

    def move(self, dx, dy):
        """機体を(dx, dy)だけ移動させる"""
        self.rect.move_ip(dx, dy)

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        if not self.gun.isBulletZero():     # 残弾数が0でないなら弾を発射する
            self.gun.shoot(x, y)

    def reload(self):
        self.gun.reload()
    
    def Tracking_shoot(self, x, y):
        self.gun2.shoot(x, y)
    
    def Opposite_shoot(self, x, y):
        self.gun3.shoot(x, y)
    
    def Reflection_shoot(self, x, y):
        self.gun4.shoot(x, y)

    def Circle_shoot(self, x, y):
        self.gun5.shoot(x, y)

    def hit(self, attack):
        """引数attack分だけ機体にダメージを与え、hpがなくなればすべてのグループからこの機体を削除"""
        if self.hp.damage(attack):
            self.score.add_score(10)
            self.kill()

    def isMachine(self):
        # このクラスは機体
        return True

    def recover(self, num):
        self.hp.recover(num)        # 引数で指定した値だけ体力が回復する。

    def speedDown(self, dx, dy):
        if self.dx - dx <= 0:
            dx = 0
        if self.dy - dy <= 0:
            dy = 0
        self.dx -= dx
        self.dy -= dy
        return dx, dy

    def speedUp(self, dx, dy):
        if self.dx != 0:
            self.dy += dx
        if self.dy != 0:
            self.dx += dy
        return dx, dy