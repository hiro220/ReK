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
        self.move_timer = []
        self.natural = True
        self.shoot_flag = False
        self.shoot_times = 0
        self.move_count = {0:0, 1:0, 2:0, 3:0}
        self.move_dic = {0:Move_pack0(self), 3:Move_pack3(self), 8:Move_pack8(self),10:Move_pack10(self), 11:Move_pack11(self), 12:Move_pack12(self),100:Move_flesh(self)}
        if sub_number == 0:
            self.gun = Division_Gun(self.machines, self,-1, 500)
        else:
            self.gun = Division_Gun(self.machines, self,-1, 500)

    def update(self):
        
        if self.natural:
            self.move_rutin(2)
            self.natural = False
        
        if self.shoot_flag and self.shoot_times != 0:
            print("test2")
            super().shoot(self.rect.left, self.rect.top)
            self.shoot_times -= 1
        #print(self.shoot_flag)
        self.move_select(self.sel_number)
        self.move(self.dx,self.dy)
        
    def move_select(self, select_number):
        self.move_dic[select_number].move()
                                                        #カウントする回数 次にするパックナンバー
    def change_number(self, number,boolean=False, times=0, option=[False,None]):
        self.sel_number = number
        self.shoot_flag = boolean
        self.shoot_times = times
        if option[0]:
            self.move_dic[self.sel_number].change_option(option)
    
    def del_timer(self, number="all"):
        if number == "all":
            for t_list in self.move_timer:
                t_list.kill()
        for index,t_list in enumerate(self.move_timer):
            if t_list.arg[0] == number:
                self.move_timer[index].kill()

    def move_rutin(self, number):
        if number == 0:
            self.move_timer.append(Timer(3000, self.change_number, 8))
            self.move_timer.append(Timer(4000, self.change_number, 100, True, 1))
            self.move_timer.append(Timer(9000, self.change_number, 8))
            self.move_timer.append(Timer(10000, self.change_number, 100, True, 1))
            self.move_timer.append(Timer(15000, self.change_number, 8))
            self.move_timer.append(Timer(16000, self.change_number, 100))
        elif number == 1:
            self.move_timer.append(Timer(2000, self.change_number, 10))
            self.move_timer.append(Timer(3000, self.change_number, 3, True ,-1))
            #self.move_timer.append(Timer(4000, self.change_number, 100, True, -1))
        elif number == 2:
            self.move_timer.append(Timer(2000, self.change_number, 12))
            self.move_timer.append(Timer(3000, self.change_number, 11, True ,-1))
    
class Move_Pack:
    def __init__(self, principal):
        self.sub = principal
        self.option = None
        self.count = 0
        
    def change_option(self, option):
        self.option = option

class Move_flesh(Move_Pack):
    def move(self):
        self.sub.dx,self.sub.dy = 0, 0

class Move_pack0(Move_Pack):
    def move(self):
        self.sub.dx,self.sub.dy = self.sub.boss.dx,self.sub.boss.dy
    
class Move_pack1(Move_Pack):
    def move(self): 
        self.sub.dx,self.sub.dy = self.sub.boss.rect.centerx - self.sub.rect.centerx, self.sub.boss.rect.centery - self.sub.rect.centery
        if self.number == 0:
            self.sub.dy -= 100
        elif self.number == 1:
            self.sub.dy += 100
        self.sub.natural = True

class Move_pack2(Move_Pack):            
    def move(self): #画面後方に配置
        self.dx,self.dy = mg2.right - self.rect.right, mg2.centery - self.rect.centery
        if self.number == 0:
            self.dx -= 50
            self.dy -= 200
        if self.number == 1:
            self.dx -= 50
            self.dy += 200
        self.sel_number = 1

class Move_pack3(Move_Pack):
    def __init__(self, principal):
        super().__init__(principal)
        self.random = []
        
    def move(self): #後ろから前に移動
        self.sub.dx,self.sub.dy = -10,0
        if self.sub.rect.right <= mg2.left:
            self.sub.rect.left = mg2.right
            #if self.option[0]:
                #self.count += 1
    
    def random_reset(self):
        print("んなあああああ")

class Move_pack4(Move_Pack):    
    def move(self): #boss前方に配置
        self.dx,self.dy = self.boss.rect.centerx - self.rect.centerx, self.boss.rect.centery - self.rect.centery
        if self.number == 0:
            self.dy -= 50
            self.dx -= 100
        if self.number == 1:
            self.dy += 50
            self.dx -= 100

class Move_pack5(Move_Pack):    
    def move(self): #未完成
        if self.number == 0 and self.rect.top - 30 <= mg2.top:
            self.dy = 10
        elif self.number == 0 and self.rect.bottom -30 >= mg2.centerx:
            self.dy = -10

        if self.number == 1 and self.rect.bottom + 30 >= mg2.bottom:
            self.dy = -10
        elif self.number == 1 and self.rect.top -30 <= mg2.centerx:
            self.dy = 10

class Move_pack6(Move_Pack):    
    def move(self): #前から後ろに移動
        self.dx,self.dy = 10,0
        if self.rect.left >= mg2.right:
            self.rect.right = mg2.left

class Move_pack7(Move_Pack):    
    def move(self):
        if self.number == 0:
            self.dx,self.dy = 0,-10
            if self.rect.bottom <= mg2.top:
                self.rect.top = mg2.bottom
        elif self.number == 1:
            self.dx,self.dy = 0,10
            if self.rect.top >= mg2.bottom:
                self.rect.bottom = mg2.top

class Move_pack8(Move_Pack):
    def move(self):
        #self.move_flesh()
        if self.sub.number == 0:
            self.sub.rect.center = self.sub.machines.sprites()[0].rect.centerx, 50
        if self.sub.number == 1:
            self.sub.rect.center = self.sub.machines.sprites()[0].rect.centerx, mg2.bottom -50

class Move_pack9(Move_Pack):
    def move(self):
        if self.rect.centerx - self.players.rect.centerx > 0:
            self.dx = -2
        elif self.rect.centerx - self.players.rect.centerx < 0:
            self.dx = 2

class Move_pack10(Move_Pack):    
    def move(self):
        if self.sub.number == 0:
            self.sub.rect.center = mg2.right - 50,50
        if self.sub.number == 1:
            self.sub.rect.center = mg2.right - 50,mg2.bottom - 50

class Move_pack11(Move_Pack): #画面上部で往復運動
    def move(self):
        if self.sub.number == 0:
            self.sub.dx,self.sub.dy = -10,0
            if self.sub.rect.right <= mg2.left:
                self.sub.rect.left = mg2.right
        if self.sub.number == 1:
            self.sub.dx,self.sub.dy = 10,0
            if self.sub.rect.left >= mg2.right:
                self.sub.rect.right = mg2.left

class Move_pack12(Move_Pack):
    def move(self):
        if self.sub.number == 0:
            self.sub.rect.center = mg2.right-50, mg2.top+50
        if self.sub.number == 1:
            self.sub.rect.center = mg2.left+50, mg2.top+50
