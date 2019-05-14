#!/usr/bin/env python
# coding:utf-8
from bullet import *
import pygame
from pygame.locals import *
import math

class Gun:

    def __init__(self, machines, max):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines
        self.rect = Rect(0,0,960,600)
        self.count = 0
        self.gun_start = pygame.time.get_ticks()
        

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        if self.num == 0:
            return True
        else:
            return False

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        Bullet(x, y, 10, 0, self.machines)      # 弾を生成する(BulletクラスはMainクラスでグループ化されているため、返却する必要はない)
        self.num -= 1

    def reload(self):
        self.num = self.max
    
    
class Tracking_Gun(Gun):

    def shoot(self, x, y):
        play_list = self.machines.sprites()
        for play in play_list:   
            distance = math.sqrt((play.rect.centerx-x)**2+(play.rect.centery-y)**2)
            angle = distance / 10
            Bullet(x, y, (play.rect.centerx-x)/angle,(play.rect.centery-y)/angle, self.machines)
            break
        self.num -= 1

class Opposite_Gun(Gun):

    def shoot(self, x, y):
        Bullet(x, y, -10, 0, self.machines)
        self.num -= 1
        
class Reflection_Gun(Gun):

    def shoot(self, x, y):
        Reflection_Bullet(x, y, -10, 0, self.machines)
        self.num -= 1

class Circle_Gun(Gun):
    
    def shoot(self, x, y):
        Bullet_list1 = [[-4.0,0],[-3.5,-3.5],[0,-4.0],[3.5,-3.5],[4.0,0],[3.5,3.5],[0,4.0],[-3.5,3.5]]
        Bullet_list2 = [[1.9,-4.6],[4.6,-1.9],[4.6,1.9],[1.9,4.6],[-1.9,4.6],[-4.6,1.9],[-4.6,-1.9],[-1.9,-4.6]]
        if pygame.time.get_ticks() - self.gun_start >= 1200 and self.count == 0:
            for bullet_list in Bullet_list1:
                Bullet(x, y, bullet_list[0],bullet_list[1], self.machines)
            self.gun_start = pygame.time.get_ticks()
            self.count = 1
        if  pygame.time.get_ticks() - self.gun_start >= 1200 and self.count == 1:
            for bullet_list in Bullet_list2:
                Bullet(x, y, bullet_list[0], bullet_list[1], self.machines)
            self.gun_start = pygame.time.get_ticks()
            self.count = 0
        self.num -= 1

class Twist_Gun(Gun):

    def __init__(self, machines, max):
        super().__init__(machines, max)
        self.standard_parameter = -10.0
        self.standard_angle = 0
    def shoot(self, x, y):
        
        dx = self.standard_parameter*math.cos(math.radians(self.standard_angle))
        dy = self.standard_parameter*math.sin(math.radians(self.standard_angle))
        Bullet(x, y, dx, dy, self.machines)
        if self.standard_angle >= 45:
            self.count = 1

        if self.standard_angle <= -45:
            self.count = 0

        if self.count == 0:
            self.standard_angle += 10
        if self.count == 1:
            self.standard_angle -= 10
        self.num -= 1