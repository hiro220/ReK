#!/usr/bin/env python
# coding:utf-8

import pygame
import math
from define import R_time
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/bullet1.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。

    def move(self):
        self.rect.move_ip(self.dx, self.dy)     # 弾を移動させる
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.survival_flag = 1
                machine.hit(1)

class Reflection_Bullet(Bullet):
    
    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/bullet2.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。
        self.count = 0                  # 壁に反射した回数を保存

    def move(self):
        self.rect.move_ip(self.dx, self.dy)
        if self.rect.bottom >= 600 or self.rect.top <= 0 and self.count <= 5:
            self.dy *= -1                                      #bulletの進行方向を逆転
            self.count += 1
        elif self.rect.right >= 960 or self.rect.left <= 0 and self.count <= 5:
            self.dx *= -1                                      #bulletの進行方向を逆転
            self.count += 1
        
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)

class Missile_Bullet(Bullet):
    def __init__(self, x, y, dx, dy, machines):
        super().__init__(x, y, dx, dy, machines)
        self.gun_start = R_time.get_ticks()
        self.image = pygame.image.load("img/missile.png").convert_alpha()
        self.flag = 0

    def move(self):
        self.rect.move_ip(self.dx, self.dy)
        if R_time.get_ticks() - self.gun_start >= 600:
            play_list = self.machines.sprites()
            x, y = self.rect.midleft
            for play in play_list:
                distance = math.sqrt((play.rect.centerx - x)**2 + (play.rect.centery - y)**2)
                angle = math.degrees(math.atan2(play.rect.centery - y, x - play.rect.centerx))
                if distance >= 150 and self.flag == 0:
                    self.image = pygame.image.load("img/missile.png").convert_alpha()
                    distance2 = distance / 5
                    self.dx, self.dy = (play.rect.centerx - x) / distance2, (play.rect.centery - y) / distance2
                    self.rect.move_ip(self.dx, self.dy)
                    self.image = pygame.transform.rotate(self.image, angle)
                else:
                    self.flag = 1
                    self.rect.move_ip(self.dx, self.dy)
                    break
                    
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)


class Meteorite(Bullet):

    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/meteorite.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。
        self.count = 0                  # 壁に反射した回数を保存
