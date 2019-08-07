#!/usr/bin/env python
# coding:utf-8
from bullet import *
from beam import *
from define import R_time
import pygame
import math
import random
from timer import Timer

class Gun:

    def __init__(self, machines,principal, max):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines
        self.principal = principal                               #弾を打つ本人の位置情報
        self.count = 0
        self.gun_start = R_time.get_ticks()
        self.dx,self.dy = -10,0
        
    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        return self.num == 0

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        if self.principal.cop_flag:
            Bullet(x, y, self.dx*-1, self.dy, self.machines)      # 弾を生成する(BulletクラスはMainクラスでグループ化されているため、返却する必要はない)
        else:
            Bullet(x+self.principal.rect.width, y, self.dx*-1, self.dy, self.machines)
        self.num -= 1

    def reload(self):
        self.num = self.max                     #bulletの玉数を上限に戻す

    def BulletZero(self):    
        self.num = 0
    
class Tracking_Gun(Gun):
    def shoot(self, x, y):
        play_list = self.machines.sprites()    #相手の設定情報を入手
        for play in play_list:   
            distance = math.sqrt((play.rect.centerx-x)**2+(play.rect.centery-y)**2) #自身と相手の距離を計測
            angle = distance / 10
            Bullet(x, y, (play.rect.centerx-x)/angle,(play.rect.centery-y)/angle, self.machines) #相手の現在の場所に弾を飛ばす
            break
        self.num -= 1     #弾の残弾数を減らす                                                                       

class Opposite_Gun(Gun): #右から左に弾を飛ばす
    def shoot(self, x, y):
        if self.principal.cop_flag:
            Bullet(x-self.principal.rect.width, y, self.dx, self.dy, self.machines)
        else:
            Bullet(x, y, self.dx, self.dy, self.machines)
        self.num -= 1
        
class Reflection_Gun(Gun): #左から右に弾を飛ばす
    def __init__(self, machines,principal, max):
        super().__init__(machines,principal, max)
        if principal.cop_flag:
            self.dx = self.dx*-1

    def shoot(self, x, y):
        Reflection_Bullet(x, y, self.dx, self.dy, self.machines)
        self.num -= 1

class Circle_Gun(Gun):
    
    def shoot(self, x, y):
        Bullet_list1 = [[-4.0,0],[-3.5,-3.5],[0,-4.0],[3.5,-3.5],[4.0,0],[3.5,3.5],[0,4.0],[-3.5,3.5]]           #弾の飛ばす方向を格納
        Bullet_list2 = [[1.9,-4.6],[4.6,-1.9],[4.6,1.9],[1.9,4.6],[-1.9,4.6],[-4.6,1.9],[-4.6,-1.9],[-1.9,-4.6]] #弾の飛ばす方向を格納
        if self.count == 0:                  #弾をそれぞれ交互にとばすためのself.count
            for bullet_list in Bullet_list1:
                Bullet(x, y, bullet_list[0],bullet_list[1], self.machines)
            #self.gun_start = R_time.get_ticks()
            self.count = 1
            self.num -= 1
        elif  self.count == 1:
            for bullet_list in Bullet_list2:
                Bullet(x, y, bullet_list[0], bullet_list[1], self.machines)
            #self.gun_start = R_time.get_ticks()
            self.count = 0
            self.num -= 1

class Twist_Gun(Gun):

    def __init__(self, machines, principal, max):
        super().__init__(machines, principal, max)   #superクラス(Gun）を呼び出す
        self.standard_parameter = -10.0              #飛ばす弾の速度と角度を格納
        self.standard_angle = 0                      #飛ばす弾の角度を格納(例１５）
        self.shot_flag = True
        self.angle_count = 0
        self.shot_count = 0
        if self.principal.cop_flag:
            self.standard_parameter *= -1
            
    def shoot(self, x, y):
        #self.count_angle()
        dx = self.standard_parameter*math.cos(math.radians(self.standard_angle)) #飛ばす角度を指定してdxの値を変化させる
        dy = self.standard_parameter*math.sin(math.radians(self.standard_angle)) #飛ばす角度を指定してdyの値を変化させる
        Bullet(x, y, dx, dy, self.machines)
        #self.shot_count += 1
        if self.standard_angle >= 45:                                            #角度が45度以上になると角度の変化が反時計回りになる
            self.count = 1

        if self.standard_angle <= -45:                                           #角度が-45度以下になると角度の変化が時計回りになる
            self.count = 0

        if self.count == 0:
            self.standard_angle += 10                                            #変化角度を+10度する  
        if self.count == 1:
            self.standard_angle -= 10                                            #変化角度を-10度する
        """if self.angle_count == 3:
            self.change_flag()
            #Timer(2000,self.change_flag)
            self.angle_count = 0
            self.shot_count = 0
        print(self.angle_count)"""
        self.num -= 1
    
    def change_flag(self):
        self.shot_flag ^= True

    def count_angle(self):
        if self.standard_angle == 0:
            self.angle_count += 1

class Beam_Gun(Gun):
    def __init__(self, machines, principal, max, angle):
        super().__init__(machines, principal, max)
        self.principal.beam_flag = 0
        self.gun_start = pygame.time.get_ticks()
        self.beam_count = 0
        self.angle = angle

    def shoot(self, x, y):
        if self.principal.beam_flag == 0 and self.beam_count == 0:
            Beam_principal(x, y, self.machines, self.principal,"img/bullet/beam/beam3.png",self.angle)
            self.principal.beam_flag = 1
            self.num -= 1
            self.beam_count += 1
        elif self.principal.beam_flag == 0 and self.beam_count == 1 and pygame.time.get_ticks() - self.gun_start >= 600:
            Beam_principal(x, y, self.machines, self.principal,"img/bullet/beam/beam3.png", self.angle)
            self.principal.beam_flag = 1
            self.num -= 1

        if self.principal.beam_flag == 1:
            self.gun_start = pygame.time.get_ticks()

class Missile_Gun(Gun):

    def __init__(self, machines, principal, max):
        super().__init__(machines, principal, max)

    def shoot(self, x, y):
        if self.principal.cop_flag == 1 and R_time.get_ticks() - self.gun_start >= 1000:
            Missile_Bullet(x, y, self.dx*-1, self.dy, self.machines, 1)
            self.gun_start = R_time.get_ticks()
        elif self.principal.cop_flag == 0:
            Missile_Bullet(x, y, self.dx, self.dy, self.machines, 0)
        self.num -= 1
        
        
class Fluffy_Gun(Gun):

    def __init__(self, machines, principal, max):
        super().__init__(machines, principal, max)

    def shoot(self, x, y):
        Fluffy_Bullet(x, y, self.dx*-1, self.dy, self.machines)
        self.num -= 1

class Thunder_Gun(Gun):

    def __init__(self, machines, principal, max):
        super().__init__(machines, principal, max)

    def shoot(self, x, y):
        Thunder_Bullet(x, y, self.dx*-2, self.dy, self.machines)
        self.num -= 1
