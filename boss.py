from machine import Machine
import pygame
from define import *
from gun import *
import random

class Boss(Machine):
    def __init__(self, hp, x, y, image, players, score):
        super().__init__(hp, x, y, image, players, score) #superクラス(machine)を呼び出す
        self.dx, self.dy = 5, 5                           #bulletの移動量を指定する
        self.x, self.y = x, y                             #機体自身の位置を入力
        self.gun_start = R_time.get_ticks()               #Bossが呼ばれた時のクロック数を入力

class Stage1_boss(Boss):                                 #ボス本体の機体
    def __init__(self, x, y, players, score):
        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(1, x, y, image, players, score)         #superクラス(Boss)を呼び出す
        self.stage1_flag = 0
        self.load_count = 0
        self.move_flag = 0
        self.move_save = [[720,300],4]
        self.dx,self.dy = -1,0

    def update(self):
        self.move(self.dx, self.dy)
        if R_time.get_ticks() - self.gun_start >= 600 and self.stage1_flag == 0:
            Stage1_sub(self.x, self.y, self.machines, self.score, self.load_count, self.rect)
            self.load_count += 1
            self.gun_start = R_time.get_ticks()
        if self.load_count == 5:
            self.stage1_flag = 1

        if self.rect.left == self.move_save[0][0] and self.rect.top == self.move_save[0][1]:
            self.dx,self.dy = 0, 0
            self.move_rule()
        #print(self.rect.top, self.rect.left)
        
    def move_rule(self):
        rule0 = [[WIDTH/2,0],[720,0],[720,HEIGHT/2],[WIDTH/2,HEIGHT],[720,HEIGHT]]                                               #[720,300]
        rule1 = [[720,0],[WIDTH/2,HEIGHT/2],[720,HEIGHT/2]]                                                                      #[480,  0]
        rule2 = [[WIDTH/2,HEIGHT/2],[720,HEIGHT/2],[720,HEIGHT]]                                                                 #[480,600]
        rule3 = [[WIDTH/2,0],[WIDTH/2,HEIGHT/2],[720,HEIGHT/2],[WIDTH,HEIGHT/2],[WIDTH,0]]                                       #[720,  0]
        rule4 = [[WIDTH/2,0],[720,0],[WIDTH,0],[WIDTH/2,HEIGHT/2],[WIDTH,HEIGHT/2],[WIDTH/2,HEIGHT],[720,HEIGHT],[WIDTH,HEIGHT]] #[720,300]
        rule5 = [[WIDTH/2,HEIGHT],[WIDTH/2,HEIGHT/2],[720,HEIGHT/2],[WIDTH,HEIGHT/2],[WIDTH,HEIGHT]]                             #[720,600]
        rule6 = [[720,0],[720,HEIGHT/2],[WIDTH,HEIGHT/2]]                                                                        #[960,  0]
        rule7 = [[720,HEIGHT],[720,HEIGHT/2],[720,0],[WIDTH,0],[WIDTH,HEIGHT]]                                                   #[960,300]
        rule8 = [[720,HEIGHT],[720,HEIGHT/2],[WIDTH,HEIGHT/2]]                                                                   #[960,600]
        point_list = [[720,300],[480,0],[480,600],[720,0],[720,300],[720,600],[960,0],[960,300],[960,600]]
        move_list = [rule0,rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]

        #print(self.move_save[1])
        self.moving(move_list[self.move_save[1]],point_list)
    
    def moving(self,move_list,point_list):
        choice_move = random.choices(move_list)
        print(self.move_save,choice_move)
        self.dx,self.dy = (choice_move[0][0] - self.move_save[0][0])/100,(choice_move[0][1] - self.move_save[0][1])/100
        for index,point in enumerate(point_list):
            if choice_move[0][0] == point[0] and choice_move[0][1] == point[1]:
                self.move_save[1] = index
        self.move_save[0] = choice_move[0]

class Stage1_sub(Boss):                                  #ボス付属品の機体
    def __init__(self, x, y, players, score, sub_number, boss_principal):              
        image = pygame.image.load("img/boss1_sub.png").convert_alpha()
        super().__init__(1, x, y, image, players, score)
        self.sub_number = sub_number                     #付属品のID
        self.boss_principal = boss_principal
        self.dx, self.dy = self.boss_principal.midleft
        self.move(0, 100)


    def update(self):
        #print(self.screen)
        self.move(-2, 0)