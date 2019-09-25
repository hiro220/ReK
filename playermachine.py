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
        super().__init__(3, x, y, image, cpus, score, money)
        self.dx, self.dy = 7, 7                         # 移動量
        self.wait_flag = 0
        self.count = 0
        self.cop_flag = True
        self.equip = data["equip"]
        self.gun_data = data["gun_data"]
        self.gun_base()
        self.reload_data()
        self.gun = self.gun_file[0]
        self.key = {'UP':K_UP, 'DOWN':K_DOWN, 'LEFT':K_LEFT, 'RIGHT':K_RIGHT, \
                    'shoot':K_x, 'reload':K_v, 'gun1':K_a, 'gun2':K_s, 'gun3':K_d}
        self.gun_number = 1
        
    def move(self):
        if self.wait_flag == 0:
            self.firstmove()
        else:
            key = pygame.key.get_pressed()      # 押されたキーを受け取る
            up, down, right, left = self.key['UP'], self.key['DOWN'], self.key['RIGHT'], self.key['LEFT']
            if key[up]:                       # 矢印キー上が押されているとき(長押し)
                super().move(0, -self.dy)
            if key[down]:                     # 矢印キー下が押されているとき(長押し)
                super().move(0, self.dy)
            if key[right]:                    # 矢印キー右が押されているとき(長押し)
                super().move(self.dx, 0)
            if key[left]:                     # 矢印キー左が押されているとき(長押し)
                super().move(-self.dx, 0)
        self.rect.clamp_ip(Rect(INFO_WIDTH, 0, WIDTH-INFO_WIDTH, HEIGHT))       # 画面外に出たとき、画面内に収まるよう移動

    def shoot(self, key):
        if self.wait_flag == 0:
            return
        if key == self.key['shoot']:              # ｘキーが押されたとき弾を発射
            x, y = self.rect.midright
            super().shoot(x, y)
        elif key == self.key['reload']:
            super().reload(self.gun_number - 1)

    def change(self, key):
        if self.wait_flag == 0:
            return
        gun_number = 1 * (key==self.key['gun1']) or 2 * (key==self.key['gun2']) or 3 * (key==self.key['gun3'])
        if self.gun_file[gun_number - 1] == None:
            return
        self.gun_number = gun_number
        self.gun = self.gun_file[self.gun_number - 1]
        
    def gun_base(self):
        self.gun_file = []   
        for i in range(3):
            self.gun_num = self.equip[i]
            if self.gun_num == -1:
                self.gun_file.append(None)
            else:
                class_name = self.gun_data[self.gun_num]['name']
                bullet_count = self.gun_data[self.gun_num]['bullet_size']
                exec("self.gun_file.append(" + class_name + "(self.machines, self,"  + str(bullet_count) + "))") 
    
    def gun_search(self, class_name):
        gun_index = None
        for i in range(3):
            if self.gun_file[i].__class__.__name__ == class_name:
                gun_index = i
        return gun_index
    
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

    def reload_data(self):
        self.reload_file = []
        for i in range(3):
            equip = self.equip[i]
            if equip == -1:
                self.reload_file.append(0)
                continue
            self.reload_file.append(self.gun_data[equip]['reload_size'])        
        super().reload_base(self.reload_file)
        
