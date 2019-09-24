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
        self.move_point = random.randint(0,1)
        self.phase_flag = 1
        self.sub_rutin = None
        #self.sub_move = True
        self.natural = [True,True,True,True,True,True]
        self.move_dic = {1:self.phase1_move, 2:self.phase2_move, 2.1:self.phase2_1_move, 3:self.phase3_move}
        self.phase2_count = R_time.get_ticks()
        self.phase1_count = R_time.get_ticks()
        self.move_pose = True
        self.shoot_flag = True
        self.first_check = True
        #self.load_count = True

        self.sub1 = Stage2_sub(self.rect.centerx,self.rect.centery-100, players, self.score, 0, self, self.money)
        self.sub2 = Stage2_sub(self.rect.centerx,self.rect.centery+100, players, self.score, 1, self, self.money)

        self.gun_dic = {0:Beam_Gun(self.machines,self, -1 ,90),1:Beam_Gun(self.machines,self, -1 ,270),2:Beam_Gun(self.machines,self, -1 ,0),3:Beam_Gun(self.machines,self, -1 ,180),\
                        4:Obot_Gun(self.machines,self, -1,90,500),5:Obot_Gun(self.machines,self,-1,270,500),6:Division_Gun(self.machines,self, -1,1200,True),7:Division_Gun(self.machines,self, -1,1500, True),\
                        8:Circle_Gun(self.machines, self, -1, 500),9:Twist_Gun(self.machines,self,-1)}
    
    def update(self):
        self.move(self.dx,self.dy)
        self.rect.clamp_ip(Rect(INFO_WIDTH, 0, WIDTH-INFO_WIDTH, HEIGHT))
        if False not in self.natural: 
            self.sub_rutin = random.randint(0,3)
        if self.first_check != True:
            self.phase_check()
            self.phase_move()

            if self.lord_flag:
                self.lord_sub()
                self.lord_flag = None
        
            if self.shoot_flag:
                super().shoot(self.rect.left, self.rect.top)
        elif self.first_check and self.rect.centerx <= mg2.right - 200:
            self.first_check = False
        
        #print(self.rect)
    
    def lord_sub(self):
        for number in range(3,7):
            Stage2_sub(mg2.centerx,100*(number-2), self.machines, self.score, number, self, self.money)
    
    def phase_check(self):
        if self.hp.hp <= 5 and self.phase_flag == 1:
            self.phase_flag = 2
    
    def phase_move(self):
        if self.phase_flag == 1 or self.phase_flag == 2 or self.phase_flag == 2.1 or self.phase_flag == 3:
            self.move_dic[self.phase_flag]()
    
    def phase_change(self, number):
        self.phase_flag = number
        
    def in_count(self):
        self.phase1_count = R_time.get_ticks()

    def phase1_move(self):
        phase1_dic = {0:Rect(850,100,210,400),1:Rect(850,100,210,400),2:Rect(850,100,210,400),3:Rect(850,100,210,400)}
        if self.rect.top <= phase1_dic[0].top or self.rect.bottom >= phase1_dic[0].bottom:
            self.dy *= -1  
        elif self.rect.left <= phase1_dic[0].left or self.rect.right >= phase1_dic[0].right:
            self.dx *= -1
        elif R_time.get_ticks() - self.phase1_count <= 1200:
            self.dx,self.dy = 0,0
            self.move_pose = True
        elif self.move_pose:
            self.dx,self.dy = random.choice([0,-3,2]), random.choice([0,-3,2])
            self.move_pose = False
            Timer(3000,self.in_count)
        
    def phase2_move(self):
        self.natural = [False,False,False,False,False]
        if self.sub1.sel_number == 99 and self.sub2.sel_number == 99:
            self.dx,selfdy = 0,0
            self.phase_flag += 0.1
            Timer(1200,self.phase_change, 2.1)
            Timer(12000,self.phase_change, 3)
            self.phase_flag = None
    def phase2_1_move(self):
        if self.rect.top <= mg2.top + 50:
            self.dy = 2
            self.phase2_count = R_time.get_ticks()
        elif self.rect.bottom >= mg2.bottom - 50:
            self.dy = -2
            self.phase2_count = R_time.get_ticks()
        elif R_time.get_ticks() - self.phase2_count >= 600:
            boolean = random.randint(0,1)
            self.phase2_count = R_time.get_ticks()
            if boolean:
                self.dy = -2
            else:
                self.dy = 2
        
    def phase3_move(self):
        self.dy = 0
        self.sub1.shoot_flag = False
        self.sub2.shoot_flag = False
        self.sub1.del_timer()
        self.sub2.del_timer()
        self.natural = [True,True,True,True,True,True]
        self.phase_flag += 0.1
    
class Stage2_sub(Boss):
    def __init__(self, x, y, players, score, sub_number, boss, money):              
        image = pygame.image.load(img_path+"bot.png").convert_alpha()
        super().__init__(100000, x, y, image, players, score, money)
        self.boss = boss
        self.number = sub_number
        self.sel_number = 0
        self.lord_count = 0
        self.move_timer = []
        self.shoot_flag = False
        self.shoot_times = 0
        self.move_dic = {0:Move_pack0(self),1:Move_pack1(self), 3:Move_pack3(self), 8:Move_pack8(self),10:Move_pack10(self), 11:Move_pack11(self), 12:Move_pack12(self),\
                        13:Move_pack13(self,self.boss.move_point),16:Move_pack16(self), 17:Move_pack17(self,self.boss.move_point),\
                        18:Move_pack18(self), 99:Move_phase2(self), 100:Move_flesh(self)}

    def update(self):
        if self.boss.natural[self.number] and len(self.move_timer) == 0:
            #self.move_rutin(self.boss.sub_rutin)
            self.move_rutin(3)
            self.boss.natural[self.number] = False

        if self.boss.hp.hp <= 5 and self.boss.phase_flag == 2:
            self.del_timer()
            self.sel_number = 99
            self.move_timer.append(Timer(1200, self.change_number, 99, True, -1,[8,8]))
            
        if self.shoot_flag and self.shoot_times != 0:
            super().shoot(self.rect.left, self.rect.top)
            self.shoot_times -= 1
        self.move_select(self.sel_number)
        self.rect.clamp_ip(Rect(INFO_WIDTH, 0, WIDTH-INFO_WIDTH, HEIGHT))
        self.move(self.dx,self.dy)

        #print(self.move_timer)
        
        
    def move_select(self, select_number):
        if select_number == None:
            return
        self.move_dic[select_number].move()

    def move_reset(self, select_number):
        self.move_dic[select_number].__init__(self)
                                                        #カウントする回数 次にするパックナンバー
    def change_number(self, number,boolean=False, times=0, gun_number=[None,None],option=[False,None]):
        self.sel_number = number
        self.shoot_flag = boolean
        self.shoot_times = times
        if any(gun_number):
            self.change_gun(gun_number)
        if option[0]:
            self.move_dic[self.sel_number].change_option(option)
    
    def change_gun(self, gun_number): #最終的にfor文で回す
        if self.number == 0 and gun_number[0] != None:
            self.gun = self.boss.gun_dic[gun_number[0]]
        if self.number == 1 and gun_number[1] != None:
            self.gun = self.boss.gun_dic[gun_number[1]]

    def del_timer(self, number=0):
        if number == 0:
            for t_list in self.move_timer:
                t_list.kill()
            self.move_timer.clear()
        """for index,t_list in enumerate(self.move_timer):
            if t_list.arg[0] == number:
                self.move_timer[index].kill()"""

    def move_rutin(self, number):
        if number == 0:
            self.move_timer.append(Timer(3000, self.change_number, 8, True, 1,[0,1]))
            self.move_timer.append(Timer(4500, self.change_number, 100))
            self.move_timer.append(Timer(5500, self.change_number,13))
            self.move_timer.append(Timer(7000, self.change_number, 100))
            self.move_timer.append(Timer(9000, self.change_number, 16, True, 1,[2,3]))
            self.move_timer.append(Timer(10500, self.change_number, 100))
            self.move_timer.append(Timer(11500, self.change_number,17))
            self.move_timer.append(Timer(13000, self.change_number, 100))
            self.move_timer.append(Timer(15000, self.change_number, 1))
        elif number == 1:
            self.move_timer.append(Timer(2000, self.change_number, 10))
            self.move_timer.append(Timer(3000, self.change_number, 3, True ,-1,[5,4]))
            self.move_timer.append(Timer(10000, self.change_number, 1))
            #self.move_timer.append(Timer(4000, self.change_number, 100, True, -1))
        elif number == 2:
            self.move_timer.append(Timer(2000, self.change_number, 12))
            self.move_timer.append(Timer(3000, self.change_number, 11, True ,-1,[6,7]))
            self.move_timer.append(Timer(10000, self.change_number, 1))
        elif number == 3:
            self.move_timer.append(Timer(2000, self.change_number, 10))
            self.move_timer.append(Timer(3000, self.change_number, 18))
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

class Move_phase2(Move_Pack):
    def move(self): 
        if self.sub.number == 0:
            self.sub.rect.center = self.sub.boss.rect.centerx, self.sub.boss.rect.centery - 100
        elif self.sub.number == 1:
            self.sub.rect.center = self.sub.boss.rect.centerx, self.sub.boss.rect.centery + 100

class Move_pack0(Move_Pack):
    def move(self):
        self.sub.dx,self.sub.dy = self.sub.boss.dx,self.sub.boss.dy
    
class Move_pack1(Move_Pack):
    def move(self): 
        if self.sub.number == 0:
            self.sub.rect.center = self.sub.boss.rect.centerx, self.sub.boss.rect.centery - 100
        elif self.sub.number == 1:
            self.sub.rect.center = self.sub.boss.rect.centerx, self.sub.boss.rect.centery + 100
        #self.sub.dx,self.sub.dy = self.sub.boss.dx,self.sub.boss.dy
        #print(self.sub.move_timer)
        self.sub.del_timer()
        self.sub.boss.natural[self.sub.number] = True
        self.sub.sel_number = None

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
        if self.sub.rect.left <= mg2.left:
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
        self.sub.dx, self.sub.dy = 0,0
        if self.sub.number == 0:
            self.sub.rect.center = self.sub.machines.sprites()[0].rect.centerx - 100, 50
        if self.sub.number == 1:
            self.sub.rect.center = self.sub.machines.sprites()[0].rect.centerx + 100, mg2.bottom -50

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
            if self.sub.rect.left <= mg2.left:
                self.sub.rect.left = mg2.right
        if self.sub.number == 1:
            self.sub.dx,self.sub.dy = 10,0
            if self.sub.rect.right >= mg2.right:
                self.sub.rect.right = mg2.left

class Move_pack12(Move_Pack):
    def move(self):
        if self.sub.number == 0:
            self.sub.rect.center = mg2.right-50, mg2.top+50
        if self.sub.number == 1:
            self.sub.rect.center = mg2.left+50, mg2.top+50

class Move_pack13(Move_Pack): #ランダム横移動
    def __init__(self, principal, point):
        super().__init__(principal)
        self.point = point

    def move(self):
        if self.point:
            self.sub.dx,self.sub.dy = -5,0
        else:
            self.sub.dx,self.sub.dy = 5,0

class Move_pack16(Move_Pack): #横配置
    def move(self):
        if self.sub.number == 0:
            self.sub.rect.center = mg2.centerx + 200, self.sub.machines.sprites()[0].rect.centery - 100
        if self.sub.number == 1:
            self.sub.rect.center = mg2.left + 50,self.sub.machines.sprites()[0].rect.centery + 100

class Move_pack17(Move_Pack): #ランダム縦移動
    def __init__(self, principal, point):
        super().__init__(principal)
        self.point = point

    def move(self):
        if self.point:
            self.sub.dx,self.sub.dy = 0,-5
        else:
            self.sub.dx,self.sub.dy = 0,5

class Move_pack18(Move_Pack):
    def __init__(self, principal):
        super().__init__(principal)
        self.p_point = [None,None]
        self.change_flag = True
        self.angle = None
        self.player = self.sub.machines.sprites()[0]
    def move(self):
        if self.change_flag:
            self.p_set()
            self.angle_set()
            self.move_set()
            self.change_flag = False
        if self.sub.rect.bottom >= mg2.bottom or self.sub.rect.top <= mg2.top or self.sub.rect.left <= mg2.left or self.sub.rect.right >= mg2.right:
            self.sub.dx, self.sub.dy = 0 ,0
            self.change_flag = True
    
    def p_set(self):
        self.p_point[0],self.p_point[1] = self.player.rect.centerx, self.player.rect.centery

    def move_set(self):
        self.sub.dx,self.sub.dy = int(-30*math.cos(self.angle)), int(-30*math.sin(self.angle))
    
    def angle_set(self):
        distance_x = (self.sub.rect.centerx - self.p_point[0])/10
        distance_y = (self.sub.rect.centery - self.p_point[1])/10
        self.angle = math.atan2(distance_y,distance_x)