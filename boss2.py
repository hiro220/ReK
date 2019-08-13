from boss import Boss
import pygame
from define import *
from item import *
from gun import *
from timer import *
import random
import math

img_path = "img/cpu/"

class Stage2_boss(Boss):
    def __init__(self, x, y, players, score, money):
        image = pygame.image.load(img_path+"cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10, x, y, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.dx,self.dy = -2, 0
        self.score = score
        self.money = money
        self.lord_flag = False
        #self.load_count = True

        Stage2_sub(self.rect.centerx,self.rect.centery-100, players, self.score, 0, self, self.money)
        Stage2_sub(self.rect.centerx,self.rect.centery+100, players, self.score, 1, self, self.money)
    
    def update(self):
        if self.rect.centerx <= 1000:
            self.dx = 0
        self.move(self.dx,self.dy)
        
        if self.hp.hp <= 5 and self.lord_flag == False:
            self.lord_flag = True

        if self.lord_flag:
            self.lord_sub()
            self.lord_flag = None
    
    def lord_sub(self):
        for number in range(3,7):
            Stage2_sub(mg2.centerx,100*(number-2), self.machines, self.score, number, self, self.money)

class Stage2_sub(Boss):
    def __init__(self, x, y, players, score, sub_number, boss, money):              
        image = pygame.image.load(img_path+"bot.png").convert_alpha()
        super().__init__(5, x, y, image, players, score, money)
        self.boss = boss
        self.number = sub_number
        self.sel_number = 0
        self.lord_count = 0
        self.move_dic = {0:self.move_pack0, 1:self.move_pack1, 2:self.move_pack2, 3:self.move_pack3, 4:self.move_pack4, 5:self.move_pack5, \
        6:self.move_pack6, 7:self.move_pack7, 8:self.move_pack8, 100:self.move_flesh}
        Timer(3000,self.change_number, 8)

    def update(self):
        self.move_select(self.sel_number)
        self.move(self.dx,self.dy)
    
    def move_select(self, select_number):
        self.move_dic[select_number]()

    def change_number(self,number):
        self.sel_number = number
    
    def move_flesh(self):
        self.dx,self.dy = 0, 0
    
    #def setting_sub(self):

    
    def move_pack0(self):
        self.dx,self.dy = self.boss.dx,self.boss.dy
    
    def move_pack1(self): 
        self.dx,self.dy = self.boss.rect.centerx - self.rect.centerx, self.boss.rect.centery - self.rect.centery
        if self.number == 0:
            self.dy -= 100
        elif self.number == 1:
            self.dy += 100
            
    def move_pack2(self): #画面後方に配置
        self.dx,self.dy = mg2.right - self.rect.right, mg2.centery - self.rect.centery
        if self.number == 0:
            self.dx -= 50
            self.dy -= 200
        if self.number == 1:
            self.dx -= 50
            self.dy += 200
        self.sel_number = 1
    
    def move_pack3(self): #前から後ろに移動
        self.dx,self.dy = -10,0
        if self.rect.right <= mg2.left:
            self.rect.left = mg2.right
    
    def move_pack4(self): #boss前方に配置
        self.dx,self.dy = self.boss.rect.centerx - self.rect.centerx, self.boss.rect.centery - self.rect.centery
        if self.number == 0:
            self.dy -= 50
            self.dx -= 100
        if self.number == 1:
            self.dy += 50
            self.dx -= 100
    
    def move_pack5(self): #未完成
        if self.number == 0 and self.rect.top - 30 <= mg2.top:
            self.dy = 10
        elif self.number == 0 and self.rect.bottom -30 >= mg2.centerx:
            self.dy = -10

        if self.number == 1 and self.rect.bottom + 30 >= mg2.bottom:
            self.dy = -10
        elif self.number == 1 and self.rect.top -30 <= mg2.centerx:
            self.dy = 10
    
    def move_pack6(self): #前から後ろに移動
        self.dx,self.dy = 10,0
        if self.rect.left >= mg2.right:
            self.rect.right = mg2.left
    
    def move_pack7(self):
        if self.number == 0:
            self.dx,self.dy = 0,-10
            if self.rect.bottom <= mg2.top:
                self.rect.top = mg2.bottom
        elif self.number == 1:
            self.dx,self.dy = 0,10
            if self.rect.top >= mg2.bottom:
                self.rect.bottom = mg2.top

    def move_pack8(self):
        self.move_flesh()
        if self.number == 0:
            self.rect.center = self.machines.sprites()[0].rect.centerx, 100
        if self.number == 1:
            self.rect.center = self.machines.sprites()[0].rect.centerx, mg2.bottom -100
