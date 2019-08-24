# coding:utf-8

from machine import Machine
import pygame
from pygame.locals import *
from gun import *
from define import INFO_WIDTH, WIDTH, HEIGHT

class PlayerMachine(Machine):
    killed_count = 0
    def __init__(self, x, y, cpus, score, money, data):
        """引数は、初期位置(x, y)、弾の当たり判定対象となる敵機グループ"""
        image = pygame.image.load("img/player.png").convert_alpha()
        super().__init__(2, x, y, image, cpus, score, money)
        self.dx, self.dy = 7, 7                         # 移動量
        self.wait_flag = 0
        self.count = 0
        self.cop_flag = True
        self.equip = data["equip"]
        self.gun_data = data["gun_data"]
        self.gun_base()
        self.gun = self.gun_file[0]
        self.gun = Laser_Gun(self.machines, self, 100)
        
    def move(self):
        if self.wait_flag == 0:
            self.firstmove()
        else:
            key = pygame.key.get_pressed()      # 押されたキーを受け取る
            if key[K_UP]:                       # 矢印キー上が押されているとき(長押し)
                super().move(0, -self.dy)
            if key[K_DOWN]:                     # 矢印キー下が押されているとき(長押し)
                super().move(0, self.dy)
            if key[K_RIGHT]:                    # 矢印キー右が押されているとき(長押し)
                super().move(self.dx, 0)
            if key[K_LEFT]:                     # 矢印キー左が押されているとき(長押し)
                super().move(-self.dx, 0)
        self.rect.clamp_ip(Rect(INFO_WIDTH, 0, WIDTH-INFO_WIDTH, HEIGHT))       # 画面外に出たとき、画面内に収まるよう移動

    def shoot(self, key):
        if key == K_x:              # ｘキーが押されたとき弾を発射
            x, y = self.rect.midright
            super().shoot(x, y)
        elif key == K_v:
            super().reload()

    def change(self, key):
        gun_number = 1 * (key==K_a) or 2 * (key==K_s) or 3 * (key==K_d)
        if gun_number == 0 or self.gun_file[gun_number - 1] == None:
            return
        self.gun = self.gun_file[gun_number - 1]
        
    def gun_base(self):
        self.gun_file = []   
        for i in range(3):
            gun_num = self.equip[i]
            if gun_num == -1:
                self.gun_file.append(None)
            else:
                class_name = self.gun_data[gun_num]['name']
                bullet_count = self.gun_data[gun_num]['bullet_size']
                exec("self.gun_file.append(" + class_name + "(self.machines, self,"  + str(bullet_count) + "))") 
            
    
    def isGameOver(self):
        return not self.alive()

    def firstmove(self):
        super().BulletZero()   
        super().move(5, 0)                
        pygame.display.update()
        self.count += 1
        if self.count == 20:
            self.gun.reload()
            self.wait_flag = 1

    def death(self):
        PlayerMachine.killed_count += 1