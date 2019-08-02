#!/usr/bin/env python
# coding:utf:-8

import pygame
from gun import *
from timer import Timer, FlagTimer
from define import WIDTH, HEIGHT
from random import random, randrange

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

    def __init__(self, hp, x, y, img, machines, score, money):
        """引数は、機体の体力を表すhp、機体の初期位置(x, y)、描画する画像、発射する弾の当たり判定対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.hp = Hp(hp)
        self.image = img            # 引数の画像をインスタンス変数に保存する
        self.rect = img.get_rect()  # 画像からrectを取得する
        self.rect.move_ip(x, y)     # 初期位置に移動させる
        self.gun = Gun(machines, self, 10)    # Gunクラスのインスタンスを生成する
        self.machines = machines
        self.survival_flag = 0      #マシンが存在しているかを判定
        self.beam_flag = 0          #ビームが存在しているかを判定
        self.reload_flag = True
        self.cop_flag = 0
        self.flagtimer = FlagTimer(lambda x:x, 0)

        self.dx = self.dy = 0
        self.score = score
        self.money = money

    def move(self, dx, dy):
        """機体を(dx, dy)だけ移動させる"""
        self.rect.move_ip(dx, dy)

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        if not self.gun.isBulletZero():     # 残弾数が0でないなら弾を発射する
            self.gun.shoot(x, y)

    def reload(self):
        self.gun.reload()
        if self.reload_flag:
            self.reload_flag = False
            bullet_num = self.gun.num
            bullet_num /= self.gun.max/10
            self.gun.num = 0
            Timer(1000+bullet_num*500, self.gun.reload)
            Timer(1500+bullet_num*500, self.change_flag)
    
    def BulletZero(self):
        self.gun.BulletZero()

    def change_flag(self):
        self.reload_flag = True
    
    def hit(self, attack, lasting=False):
        """引数attack分だけ機体にダメージを与え、hpがなくなればすべてのグループからこの機体を削除
        機体に対して持続的にダメージを与えるときはlastingをTrueにする。
        """
        if self.hp.damage(attack):
            self.score.add_score(10)
            self.survival_flag = 1
            self.money.add_money(100)
            self.death()
            self.kill()
            self.flagtimer.kill()
        else:
            # ダメージを受けたが、破壊されていないなら、一定時間無敵になる
            if len(self.flagtimer.groups()) == 0:
                self.flagtimer = FlagTimer(self.invincible, 1500, flag=lasting)
            else:
                self.flagtimer.flag = lasting

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
    
    def set_image(self, image):
        self.image = image

    def invincible(self, millisecond):
        if len(self.groups()) != 3:
            return
        alpha = 100                         # 透明度
        tmp_image = self.image.copy()       # 元の画像をコピー
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)       # 指定の透明度に設定する
        Timer(millisecond, self.set_image, tmp_image)      # 一定時間経過後、元の画像に戻す
        group = self.groups()[2]            # 当たり判定用のグループ
        self.remove(group)                  # この機体を当たり判定のグループから取り除く
        Timer(millisecond, self.add_group, group)                 # 一定時間経過後、グループに戻す
    
    def add_group(self, group):
        if len(self.groups()) != 2:
            return
        self.add(group)

    def fall_meteorite(self, machines, num, millisecond):
        x, y = WIDTH, 0
        if random() < 0.5:
            x = randrange(200, WIDTH, 1)
        else:
            y = randrange(200, HEIGHT-200, 1)
        Meteorite(x, y, -12, 8, machines)
        if num-1 == 0:
            return
        Timer(millisecond, self.fall_meteorite, machines, num-1, millisecond)