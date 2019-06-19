from machine import Machine
import pygame
from define import *
from item import *
from gun import *
from timer import *
import random
import math

class Boss(Machine):
    def __init__(self, hp, x, y, image, players, score):
        super().__init__(hp, x, y, image, players, score) #superクラス(machine)を呼び出す
        self.dx, self.dy = 5, 5                           #bulletの移動量を指定する
        self.x, self.y = x, y                             #機体自身の位置を入力
        self.gun_start = R_time.get_ticks()               #Bossが呼ばれた時のクロック数を入力

class Stage1_boss(Boss):                                 #ボス本体の機体
    def __init__(self, x, y, players, score):
        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10000, x, y, image, players, score)         #superクラス(Boss)を呼び出す
        self.shield  = Timer(0,Shield,10000,self)
        self.summon_flag = 0
        self.load_count = 0
        self.move_flag = 0
        self.clear_flag = 0
        self.invincible_flag = 0
        self.invin_start = R_time.get_ticks()
        self.move_save = [[680,280],4]
        self.dx,self.dy = -2,0
        self.shot_list = []

    def update(self):
        self.move(self.dx, self.dy)
        self.Invincible()                                           #バリアとマシンのHPを設定しなおす
        self.Invincible2()                                          #HPが５以下の時無敵を生成する
        self.Move_set()                                             #HPが５以下になるとボスの位置を戻す
        
        if R_time.get_ticks() - self.gun_start >= 140 and self.summon_flag == 1:
            Stage1_sub(610, 600, self.machines, self.score, self.load_count, self)
            self.load_count += 1
            self.gun_start = R_time.get_ticks()
        if self.load_count == 18:
            self.summon_flag = None

        if self.rect.left == self.move_save[0][0] and self.rect.top == self.move_save[0][1]:
            self.dx,self.dy = 0, 0
            if self.move_flag == 0:
                self.move_rule()
            elif self.move_flag == 1:
                self.clear_flag = 1
                self.summon_flag = 1
                self.move_flag = 2
                self.gun_start = R_time.get_ticks()
        
        if R_time.get_ticks() - self.gun_start >= 3500 and self.load_count == 18:
            self.move_flag = 0
        if self.move_flag == 0 and self.summon_flag == None and R_time.get_ticks() - self.gun_start >= 1200:
            self.shot_list = random.sample(range(18), k=4)
            self.gun_start = R_time.get_ticks() 

        self.Shield_loop()                                      #シールドを再配置する
               
        #print(self.groups()[1])
        #print(self.move_flag)
        #print(self.dx,self.dy)
        #print(self.rect.left,self.rect.top)
        #print(mg.centerx,mg.centery)
        #print(self.clear_flag)
        print(self.hp.hp)
        
    def move_rule(self):
        rule0 = [[mg.centerx,mg.top],[mg.left,mg.centery],[mg.centerx,mg.centery]]                                            #[440, 40]
        rule1 = [[mg.left,mg.top],[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.left,mg.bottom]]     #[440,280]
        rule2 = [[mg.left,mg.centery],[mg.centerx,mg.centery],[mg.centerx,mg.bottom]]                                         #[440,520]
        rule3 = [[mg.left,mg.top],[mg.left,mg.centery],[mg.centerx,mg.centery],[mg.right,mg.centery],[mg.right,mg.top]]       #[680, 40]
        rule4 = [[mg.left,mg.top],[mg.left,mg.centery],[mg.left,mg.bottom],[mg.centerx,mg.bottom],[mg.right,mg.bottom],[mg.right,mg.centery],[mg.right,mg.top],[mg.centerx,mg.top]] #[720,300]
        rule5 = [[mg.left,mg.bottom],[mg.left,mg.centery],[mg.centerx,mg.centery],[mg.right,mg.centery],[mg.right,mg.bottom]] #[680,520]
        rule6 = [[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.right,mg.centery]]                                           #[920, 40]
        rule7 = [[mg.right,mg.top],[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.right,mg.bottom]]   #[960,300]
        rule8 = [[mg.centerx,mg.bottom],[mg.centerx,mg.centery],[mg.right,mg.centery]]                                        #[960,600]
        point_list = [[440,40],[440,280],[440,520],[680,40],[680,280],[680,520],[920,40],[920,280],[920,520]]
        move_list = [rule0,rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]

        self.moving(move_list[self.move_save[1]],point_list)

    def moving(self,move_list,point_list):
        choice_move = random.choices(move_list)
        self.dx,self.dy = (choice_move[0][0] - self.move_save[0][0])/100,(choice_move[0][1] - self.move_save[0][1])/100
        for index,point in enumerate(point_list):
            if choice_move[0][0] == point[0] and choice_move[0][1] == point[1]:
                self.move_save[1] = index
        self.move_save[0] = choice_move[0]
    
    def move_clear(self):
        x,y = mg.centerx - self.rect.left,mg.centery - self.rect.top
        if x == 0 and y > 0:
            self.dx,self.dy = 0,2
        elif x == 0 and y < 0:
            self.dx,self.dy = 0,-2
        elif y == 0 and x > 0:
            self.dx,self.dy = 2,0
        elif y == 0 and x < 0:
            self.dx,self.dy = -2,0
        elif x > 0 and y > 0:
            self.dx,self.dy = 2,2
        elif x > 0 and y < 0:
            self.dx,self.dy = 2,-2
        elif x < 0 and y > 0:
            self.dx,self.dy = -2,2
        elif x < 0 and x < 0:
            self.dx,self.dy = -2,-2
        self.move_save = [[680,280],4]

    def Invincible(self):
        if R_time.get_ticks() - self.invin_start >= 3000 and self.invincible_flag == 0:
            self.shield.value.hp.__init__(5)
            self.hp.__init__(10)
            self.invincible_flag = 1
    
    def Invincible2(self):
        if self.hp.hp <= 5 and self.invincible_flag == 1:
            self.hp.__init__(10000)
            self.invin_start = R_time.get_ticks()
            self.invincible_flag = 2
        elif R_time.get_ticks() - self.invin_start >= 10000 and self.invincible_flag == 2:
            self.hp.__init__(5)
            self.invincible_flag = None
    
    def Move_set(self):
        if self.invincible_flag == 2 and self.clear_flag == 0:
            self.move_flag = 1
            self.move_clear()

    def Shield_loop(self):
        if self.shield.value != None:
            if self.hp.hp > 5 and self.shield.value.hp.hp == 0:
                self.shield = Timer(5000,Shield,5,self)
        elif self.invincible_flag == 2:
            self.shield.kill()

class Stage1_sub(Boss):                                  #ボス付属品の機体
    def __init__(self, x, y, players, score, sub_number, boss):              
        image = pygame.image.load("img/boss1_sub.png").convert_alpha()
        super().__init__(10000, x, y, image, players, score)
        self.sub_number = sub_number                     #付属品のID
        self.boss = boss
        self.invincible_flag = 0
        self.invin_start = R_time.get_ticks()
        self.sub_count = 0
        self.rad = 0
        self.move_flag = 0
        self.dx,self.dy = 0,-4
        self.gun = Opposite_Gun(self.machines, self, 100)

    def update(self):
        self.Invincible()                           #サブマシンのHPを再設定する
        self.Kill_sub()                             #ボスが消えるとサブも消える
        if self.move_flag == 1:
            self.rad += 4
            self.dy = int(35*math.sin(math.radians(self.rad-10))) - int(35*math.sin(math.radians(self.rad)))
            self.dx = int(35*math.cos(math.radians(self.rad-10))) - int(35*math.cos(math.radians(self.rad)))
        self.move(self.dx+ int(self.boss.dx), self.dy+int(self.boss.dy))

        if self.rad >= 360:
            self.rad = 0
        if self.rect.top <= 280:
            self.move_flag =1
        if self.sub_number in self.boss.shot_list and R_time.get_ticks() - self.gun_start >= 4000:
            super().shoot(self.rect.centerx, self.rect.centery)
            self.gun_start = R_time.get_ticks()

    def Invincible(self):
        if R_time.get_ticks() - self.invin_start >= 250*self.sub_number and self.invincible_flag == 0:
            self.hp.__init__(2)
            self.invincible_flag = None
    
    def Kill_sub(self):
        if self.boss.survival_flag == 1:
            self.kill()