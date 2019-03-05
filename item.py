# coding:utf-8

import pygame
from pygame.locals import *
from machine import Hp

class Item(pygame.sprite.Sprite):
    """アイテム処理の基底となるクラス。継承するクラスは、メソッドeffect(self, machine)を定義する。
    effectメソッドでは、アイテムを取得した機体machineに対して、そのアイテムに応じた処理を行うよう記述する。"""
    def __init__(self, x, y, img, machine):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = img
        self.rect = self.image.get_rect()
        self.machine = machine                      # アイテムの効果対象
        self.speed = -1                             # アイテムの移動速度
        self.rect.move_ip(x, y)                     # 引数で指定された初期位置に移動させる

    def update(self):
        self.rect.move_ip(self.speed, 0)            # 移動
        collide_list = pygame.sprite.spritecollide(self, self.machine, False)   # 当たり判定
        if collide_list:                            # アイテムを取得した機体があるなら
            self.kill()
            for machine in collide_list:
                self.effect(machine)                # アイテムを取得した機体に対して、アイテムに応じた効果を与える

class Recovery(Item):
    """取得した機体の体力を1回復するアイテム"""
    def __init__(self, x, y, machine):
        image = pygame.image.load("img/recovery.png").convert_alpha()
        super().__init__(x, y, image, machine)

    def effect(self, machine):
        machine.recover(1)                          # 機体の体力を1回復する

class Shield(pygame.sprite.Sprite):
    """機体を守るシールド"""
    def __init__(self, firmness, machine):
        pygame.sprite.Sprite.__init__(self, machine.containers)
        self.image = pygame.image.load("img/shield.png").convert_alpha()
        self.hp = Hp(firmness*2)
        self.rect = self.image.get_rect()
        self.machine = machine
        self.update()

    def update(self):
        rect = self.machine.rect
        x1, y1 = self.rect.center
        x2, y2 = rect.center
        self.rect.move_ip(x2-x1,y2-y1)

    def hit(self, attack):
        if self.hp.damage(attack):
            self.kill()

class ShieldItem(Item):
    """取得した機体の体力を1回復するアイテム"""
    def __init__(self, x, y, machine):
        image = pygame.image.load("img/item_shield.png").convert_alpha()
        super().__init__(x, y, image, machine)

    def effect(self, machine):
        Shield(3, machine)