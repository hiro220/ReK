from machine import Machine
import pygame
from define import *
from item import *
from gun import *
from timer import *
import random
import math

class Boss(Machine):
    killed_count = 0
    def __init__(self, hp, x, y, image, players, score, money):
        super().__init__(hp, x, y, image, players, score, money) #superクラス(machine)を呼び出す
        self.dx, self.dy = 5, 5                           #bulletの移動量を指定する
        self.x, self.y = x, y                             #機体自身の位置を入力
        self.gun_start = R_time.get_ticks()               #Bossが呼ばれた時のクロック数を入力
        
    def death(self):
        Boss.killed_count += 1

class Stage1_boss(Boss):                                 #ボス本体の機体
    def __init__(self, x, y, players, score, money):
        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10000, x, 280, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.shield  = Timer(0,Shield,10000,self)
        self.summon_flag = False                         #subをロードしていいかの判定フラグ
        self.load_count = 0                              #何回subをロードかを確かめるためのフラグ
        self.move_flag = 0                               #動きていいか判定するためのフラグ
        self.clear_flag = 0                              #本体の第二形態移行時、中央戻るためのフラグ
        self.invincible_flag = 0                         #無敵時間のフラグ
        self.shot_flag = False                           #本体が打つか打たないかの判定
        self.shoot_number = 0                            #打った銃のナンバー保存場所
        self.shoot_count = 0                             #銃の打った回数を保存
        self.move_save = [[mg.centerx,mg.centery],1]     #本体の次の移動場所
        self.dx,self.dy = -2,0                           #本体の移動量
        self.shot_list = []                              #Crile_Gunを使うSub_number保存
        self.shot_list2 = []                             #追尾弾を使うSub_number保存
        self.money = money
        self.gun_list = [Circle_Gun(self.machines, self, -1),Twist_Gun(self.machines, self, -1),Beam_Gun(self.machines, self, -1)] #本体の銃リスト
        self.shoot_timer = None
        self.shoot_timing = R_time.get_ticks()
        self.gun = Circle_Gun(self.machines, self, -1)

    def update(self):
        self.move(self.dx, self.dy)
        self.Invincible()                                           #バリアとマシンのHPを設定しなおす
        self.Invincible2()                                          #HPが５以下の時無敵を生成する
        self.Move_set()                                             #HPが５以下になるとボスの位置を戻す
        
        if R_time.get_ticks() - self.gun_start >= 140 and self.summon_flag:
            Stage1_sub(mg.centerx-60, 600, self.machines, self.score, self.load_count, self, self.money)
            self.load_count += 1
            self.gun_start = R_time.get_ticks()
        if self.load_count == 18:
            self.summon_flag = None

        if self.rect.left == self.move_save[0][0] and self.rect.top == self.move_save[0][1]:
            self.dx,self.dy = 0, 0
            #ボスを一時停止するための機構
            #if random.randint(0,2) == 1:
            #self.Change_flag(1)
            #Timer(5000, self.Change_flag, 1)
            #print(self.move_flag)
            if self.move_flag == 0:
                self.move_rule()
            elif self.move_flag == 1:
                self.clear_flag = 1
                self.summon_flag = True
                self.move_flag = 2
                self.gun_start = R_time.get_ticks()
        
        if R_time.get_ticks() - self.gun_start >= 3500 and self.load_count == 18:
            self.move_flag = 0
        
        self.Cpu_shot_rule()
        self.Shield_loop()                                      #シールドを再配置する

        if self.shot_flag:
            if R_time.get_ticks() - self.shoot_timing >= 500 and self.shoot_number == 0:
                super().shoot(self.rect.left, self.rect.centery)
                self.shoot_count += 1
                self.shoot_timing = R_time.get_ticks()
            elif self.shoot_number == 1:
                super().shoot(self.rect.left, self.rect.centery)
                self.shoot_count += 1
            self.Shot_rule()
       
        #print(self.groups()[1])
        #print(self.move_flag)
        #print(self.dx,self.dy)
        #print(self.rect.left,self.rect.top)
        #print(mg.centerx,mg.centery)
        #print(self.clear_flag)
        #print(self.invincible_flag)
        #print(self.hp.hp)
        
    def move_rule(self):
        """
        rule0 = [[mg.centerx,mg.top],[mg.left,mg.centery],[mg.centerx,mg.centery]]                                            #[600, 40]
        rule1 = [[mg.left,mg.top],[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.left,mg.bottom]]     #[600,280]
        rule2 = [[mg.left,mg.centery],[mg.centerx,mg.centery],[mg.centerx,mg.bottom]]                                         #[600,520]
        rule3 = [[mg.left,mg.top],[mg.left,mg.centery],[mg.centerx,mg.centery],[mg.right,mg.centery],[mg.right,mg.top]]       #[840, 40]
        rule4 = [[mg.left,mg.top],[mg.left,mg.centery],[mg.left,mg.bottom],[mg.centerx,mg.bottom],[mg.right,mg.bottom],[mg.right,mg.centery],[mg.right,mg.top],[mg.centerx,mg.top]] #[840,280]
        rule5 = [[mg.left,mg.bottom],[mg.left,mg.centery],[mg.centerx,mg.centery],[mg.right,mg.centery],[mg.right,mg.bottom]] #[840,520]
        rule6 = [[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.right,mg.centery]]                                           #[1080, 40]
        rule7 = [[mg.right,mg.top],[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.right,mg.bottom]]   #[1080,280]
        rule8 = [[mg.centerx,mg.bottom],[mg.centerx,mg.centery],[mg.right,mg.centery]]                                        #[1080,520]
        point_list = [[mg.left,mg.top],[mg.left,mg.centery],[mg.left,mg.bottom],[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.right,mg.top],[mg.right,mg.centery],[mg.right,mg.bottom]]
        move_list = [rule0,rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]"""

        rule3 = [[mg.centerx,mg.centery],[mg.right,mg.centery],[mg.right,mg.top]]                                             #[840, 40]
        rule4 = [[mg.centerx,mg.bottom],[mg.right,mg.bottom],[mg.right,mg.centery],[mg.right,mg.top],[mg.centerx,mg.top]]     #[840,280]
        rule5 = [[mg.centerx,mg.centery],[mg.right,mg.centery],[mg.right,mg.bottom]]                                          #[840,520]
        rule6 = [[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.right,mg.centery]]                                           #[1080, 40]
        rule7 = [[mg.right,mg.top],[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.right,mg.bottom]]   #[1080,280]
        rule8 = [[mg.centerx,mg.bottom],[mg.centerx,mg.centery],[mg.right,mg.centery]]                                        #[1080,520]
        point_list = [[mg.centerx,mg.top],[mg.centerx,mg.centery],[mg.centerx,mg.bottom],[mg.right,mg.top],[mg.right,mg.centery],[mg.right,mg.bottom]]
        move_list = [rule3,rule4,rule5,rule6,rule7,rule8]

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
        self.move_save = [[mg.centerx,mg.centery],4]

    def Invincible(self):
        if self.shield.value != None and self.invincible_flag == 0:
            Timer(3000,self.shield.value.hp.__init__,5)
            Timer(3000,self.hp.__init__,10)
            Timer(3000,self.Change_flag, 0)
            self.invincible_flag = 1
    
    def Invincible2(self):
        if self.hp.hp <= 5 and self.invincible_flag == 1:
            self.hp.__init__(10000)
            if self.shot_flag:
                self.Change_flag(0)
            else:
                self.shoot_timer.kill()
            Timer(10000,self.hp.__init__,5)
            Timer(10000,self.Change_flag, 0)
            self.invincible_flag = 2
    
    def Move_set(self):
        if self.invincible_flag == 2 and self.clear_flag == 0:
            self.move_flag = 1
            self.move_clear()

    def Shield_loop(self):
        if self.shield.value != None:
            if self.hp.hp > 5 and self.shield.value.hp.hp <= 0:
                self.shield = Timer(7000,Shield,5,self)
        elif self.invincible_flag == 2:
            self.shield.kill()
    
    def Shot_rule(self):                                 #ボスの銃を変更する
        if self.shoot_number == 0 and self.shoot_count == 6:
            self.shoot_number = random.randint(0,1)
            self.gun = self.gun_list[self.shoot_number]
            self.shoot_count = 0
            self.Change_flag(0)
            self.shoot_timer = Timer(2000,self.Change_flag, 0)
        elif self.shoot_number == 1 and self.shoot_count == 15:
            self.shoot_number = random.randint(0,1)
            self.gun = self.gun_list[self.shoot_number]
            self.shoot_count = 0
            self.Change_flag(0)
            self.shoot_timer = Timer(2000,self.Change_flag, 0)
    
    def Cpu_shot_rule(self):
        if self.move_flag == 0 and self.summon_flag == None and R_time.get_ticks() - self.gun_start >= 1200:
            self.shot_list = random.sample(range(18), k=4)
            self.shot_list2 = random.sample(range(18), k=2)
            self.gun_start = R_time.get_ticks()

    def Change_flag(self, flag_number):
        if flag_number == 0 and self.shot_flag == False:
            self.shot_flag = True
        elif flag_number == 0 and self.shot_flag == True:
            self.shot_flag = False

        if flag_number == 0 and self.invincible_flag == 2:
            self.invincible_flag = None
        
        if flag_number == 1 and self.move_flag == 0:
            self.move_flag = None
        elif flag_number == 1 and self.move_flag == None:
            self.move_flag = 0

 

class Stage1_sub(Boss):                                  #ボス付属品の機体
    def __init__(self, x, y, players, score, sub_number, boss, money):              
        image = pygame.image.load("img/boss1_sub.png").convert_alpha()
        super().__init__(10000, x, y, image, players, score, money)
        self.sub_number = sub_number                     #付属品のID
        self.boss = boss
        self.invincible_flag = 0
        self.invin_start = R_time.get_ticks()
        self.sub_count = 0
        self.rad = 0
        self.move_flag = 0
        self.dx,self.dy = 0,-4
        #self.gun = Opposite_Gun(self.machines, self, 100)

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
        if  R_time.get_ticks() - self.gun_start >= 4000:
            if self.sub_number in self.boss.shot_list:
                self.gun = Opposite_Gun(self.machines, self, 100)
                super().shoot(self.rect.centerx, self.rect.centery)
                self.gun_start = R_time.get_ticks()
            elif self.sub_number in self.boss.shot_list2:
                self.gun = Tracking_Gun(self.machines, self, 100)
                super().shoot(self.rect.centerx, self.rect.centery)
                self.gun_start = R_time.get_ticks()

    def Invincible(self):
        if R_time.get_ticks() - self.invin_start >= 250*self.sub_number and self.invincible_flag == 0:
            self.hp.__init__(2)
            self.invincible_flag = None
    
    def Kill_sub(self):
        if self.boss.survival_flag == 1:
            self.kill()