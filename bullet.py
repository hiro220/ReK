#!/usr/bin/env python
# coding:utf-8

import pygame
import math
from define import R_time, INFO_WIDTH, WIDTH, HEIGHT
from timer import Timer

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.img_path = "img/bullet/"
        self.image = pygame.image.load(self.img_path+"bullet1.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。

    def move(self):
        self.rect.move_ip(self.dx, self.dy)     # 弾を移動させる
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)

class Reflection_Bullet(Bullet):
    
    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.img_path = "img/bullet/"
        self.image = pygame.image.load(self.img_path+"bullet2.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。
        self.count = 0                  # 壁に反射した回数を保存

    def move(self):
        self.rect.move_ip(self.dx, self.dy)
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0 and self.count <= 1:
            self.dy *= -1                                      #bulletの進行方向を逆転
            self.count += 1
        elif self.rect.right >= WIDTH or self.rect.left <= INFO_WIDTH and self.count <= 1:
            self.dx *= -1                                      #bulletの進行方向を逆転
            self.count += 1
        
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)

class Missile_Bullet(Bullet):

    def __init__(self, x, y, dx, dy, machines, flag):
        super().__init__(x, y, dx, dy, machines)
        self.gun_start = R_time.get_ticks()
        self.cop_flag = flag
        self.tracking_flag = 0

        if self.cop_flag:
            self.image = pygame.image.load(self.img_path+"Pmissile.png").convert_alpha()
        else:
            self.image = pygame.image.load(self.img_path+"missile.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def move(self):
        if self.cop_flag == 0:
            self.rect.move_ip(self.dx, self.dy)
            play_list = self.machines.sprites()
            x, y = self.rect.center
            for play in play_list:
                distance = math.sqrt((play.rect.centerx - x)**2 + (play.rect.centery - y)**2)
                angle = math.degrees(math.atan2(play.rect.centery - y, x - play.rect.centerx))
                if distance >= 150 and self.rect.centerx >= play.rect.centerx:
                    self.image = pygame.image.load(self.img_path+"missile.png").convert_alpha()
                    distance2 = distance / 5
                    self.dx, self.dy = (play.rect.centerx - x) / distance2, (play.rect.centery - y) / distance2
                    self.rect.move_ip(self.dx, self.dy)
                    self.image = pygame.transform.rotate(self.image, angle)
                else:
                    self.rect.move_ip(self.dx, self.dy)
                    break
        else:
            self.rect.move_ip(self.dx, self.dy)
            play_list = self.machines.sprites()
            x, y = self.rect.center

            mindistance = 1000
            for play in play_list:
                    distance = math.sqrt((play.rect.centerx - x)**2 + (play.rect.centery - y)**2)
                    if distance < mindistance:
                        mindistance = distance
                        target = play
            try:
                distance = math.sqrt((target.rect.centerx - x)**2 + (target.rect.centery - y)**2)
            except:
                return
            if distance >= 150:
                self.image = pygame.image.load(self.img_path+"Pmissile.png").convert_alpha()
                distance2 = distance / 4
                angle = math.degrees(math.atan2(y - target.rect.centery, target.rect.centerx - x))
                self.dx, self.dy = (target.rect.centerx - x) / distance2, (target.rect.centery - y) / distance2
                self.rect.move_ip(self.dx, self.dy)
                self.image = pygame.transform.rotate(self.image, angle)
            else:
                self.rect.move_ip(self.dx, self.dy)
                        
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                        # リストがあるか
            self.kill()                         # このスプライトを所属するすべてのグループから削除
            for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(1)
    
class Fluffy_Bullet(Bullet):
    
    def __init__(self, x, y, dx, dy, machines):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.img_path = "img/bullet/fluffy/"
        self.image = pygame.image.load(self.img_path+"Fluffy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.dx, self.dy = dx, dy 
        self.machines = machines
        self.maxscale = 130
        self.current_width = 47
        self.current_height = 47
        self.PI = 3.141592
        self.count = 0 
        self.swap_count = 0
        self.collide_flag = 0
        self.scale_flag = 0
        
        self.update = self.move 
        self.cycle = 0 

    def move(self):
        if self.collide_flag == 0:
            self.rect.move_ip(self.dx, self.dy)

            self.dx = 10
            self.dy = math.sin(self.PI * self.cycle/20) * 7.0

            self.cycle += 1

            #self.rect.move_ip(self.dx, self.dy)
            collide_list = pygame.sprite.spritecollide(self, self.machines, False)  
            if collide_list:
                self.collide_flag = 1
                self.dx, self.dy = self.rect.center
                for machine in collide_list:  
                    machine.hit(0.5)
        elif self.collide_flag ==  1:
            if self.swap_count == 0:
                self.image = pygame.image.load(self.img_path+"Fluffy.png").convert_alpha()
            elif self.swap_count ==  1:
                self.image = pygame.image.load(self.img_path+"Fluffy2.png").convert_alpha()
            elif self.swap_count ==  2:
                self.image = pygame.image.load(self.img_path+"Fluffy3.png").convert_alpha()
            elif self.swap_count ==  3:
                self.image = pygame.image.load(self.img_path+"Fluffy4.png").convert_alpha()
            elif self.swap_count ==  4:
                self.image = pygame.image.load(self.img_path+"Fluffy5.png").convert_alpha()
            elif self.swap_count ==  5:
                self.image = pygame.image.load(self.img_path+"Fluffy6.png").convert_alpha()
            elif self.swap_count ==  6:
                self.image = pygame.image.load(self.img_path+"Fluffy7.png").convert_alpha()
            elif self.swap_count ==  7:
                self.image = pygame.image.load(self.img_path+"Fluffy8.png").convert_alpha()
            elif self.swap_count ==  8:
                self.image = pygame.image.load(self.img_path+"Fluffy9.png").convert_alpha()
            elif self.swap_count ==  9:
                self.image = pygame.image.load(self.img_path+"Fluffy10.png").convert_alpha()

            self.image = pygame.transform.scale(self.image, (self.current_width, self.current_height))
            self.rect = self.image.get_rect()
            self.rect.move_ip(self.dx-self.rect.width/2, self.dy-self.rect.height/2)
            

            if self.scale_flag == 0:
                self.current_width += 20
                self.current_height += 20
                if self.current_width >= self.maxscale:
                    self.scale_flag = 1
                    self.max_time = R_time.get_ticks()
            if self.scale_flag == 1:
                self.current_time = R_time.get_ticks()
                if self.current_time - self.max_time >= 500:
                    self.scale_flag = 2
            if self.scale_flag == 2:
                self.current_width -= 10
                self.current_height -= 10
            
            collide_list = pygame.sprite.spritecollide(self, self.machines, False)  
            if collide_list:
                for machine in collide_list:  
                    machine.hit(0.1, lasting=True)
            if self.swap_count == 9:
                self.swap_count = 0
            else:
                self.swap_count += 1

            if self.current_width <= 0:
                self.kill()

class Thunder_Bullet(Bullet):
    
    def __init__(self, x, y, dx, dy, machines):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.img_path = "img/bullet/thunder/"
        self.image = pygame.image.load(self.img_path+"Thunder11.png").convert_alpha()
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect2 = self.rect
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        #
        self.collide_machine = 0 
        self.image_flag = 0
        self.flag = 0
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。

    def move(self):
        if self.flag == 0:
            if self.image_flag == 0:
                self.image = pygame.image.load(self.img_path+"Thunder11.png").convert_alpha()
                self.image_flag = 1
            elif self.image_flag == 1:
                self.image = pygame.image.load(self.img_path+"Thunder12.png").convert_alpha()
                self.image_flag = 0

            self.rect.move_ip(self.dx, self.dy)

            collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
            if collide_list:                        # リストがあるか
                self.flag = 1                         # このスプライトを所属するすべてのグループから削除
                for machine in collide_list:        # この弾に当たったすべての機体に対してダメージを与える
                    self.collide_machine = machine.rect
                    self.sub = subThunder_Bullet(self.collide_machine.centerx, self.collide_machine.centery, 0, 20, self.machines)
                    Timer(2000, self.kill)
                    machine.hit(0.5)
        elif self.flag == 1:
            if self.image_flag == 0:
                self.image = pygame.image.load(self.img_path+"Thunder21.png").convert_alpha()
                self.image_flag = 1
            elif self.image_flag == 1:
                self.image = pygame.image.load(self.img_path+"Thunder22.png").convert_alpha()
                self.image_flag = 0

            self.dx, self.dy = 0, -20
            self.rect.centerx = self.collide_machine.centerx
            self.rect.move_ip(self.dx, self.dy)

            self.sub.move()

            collide_list = pygame.sprite.spritecollide(self, self.machines, False)
            if collide_list:
                for machine in collide_list:
                    machine.hit(0.2)
            

class subThunder_Bullet(Bullet):
    def __init__(self, x, y, dx, dy, machines):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.img_path = "img/bullet/thunder/"
        self.image = pygame.image.load(self.img_path+"Thunder31.png").convert_alpha()
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines
        self.image_flag = 0
        
        self.update = self.move

        Timer(2000, self.kill) 

    def move(self):
        if self.image_flag == 0:
            self.image = pygame.image.load(self.img_path+"Thunder31.png").convert_alpha()
            self.image_flag = 1
        elif self.image_flag == 1:
            self.image = pygame.image.load(self.img_path+"Thunder32.png").convert_alpha()
            self.image_flag = 0

        self.rect.move_ip(self.dx, self.dy)

        collide_list = pygame.sprite.spritecollide(self, self.machines, False)
        if collide_list:
            self.flag = 1
            for machine in collide_list:
                machine.hit(0.35)


class fire_Bullet(Bullet):
    
    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/fireball1.png").convert()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.image.set_alpha(120)
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey, RLEACCEL)
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)
        self.x, self.y = x, y
        self.dx, self.dy = 10, 0       # 移動量
        self.machines = machines
        self.burning_count = 0
        self.image_num = 1
        self.shot_flag = 0
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。
        self.count = 0                  # 壁に反射した回数を保存

        Timer(3000, self.kill) 

    def move(self):
        if self.shot_flag == 0:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[K_x]:
                self.image.set_alpha(120)
                colorkey = self.image.get_at((0,0))
                self.image.set_colorkey(colorkey, RLEACCEL)
                self.rect.move_ip(self.dx, self.dy)
            else:
                self.shot_flag = 1
                self.dx, self.dy = 0, 0
                self.shot_pos = self.rect
        elif self.shot_flag == 1:
            if self.burning_count <= 40:
                text = "img/fireball{}.png"
                self.image = pygame.image.load(text.format(self.image_num)).convert()
                self.image = pygame.transform.smoothscale(self.image, (50,50))
                self.image.set_alpha(255)
                colorkey = self.image.get_at((0,0))
                self.image.set_colorkey(colorkey, RLEACCEL)
                self.image_num += 1
                if self.image_num == 9:
                    self.image_num = 1
            elif self.burning_count == 41:
                self.image_num = 1
                text = "img/fire{}.png"
                self.image = pygame.image.load(text.format(self.image_num)).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (100,110))
                self.rect = self.image.get_rect()
                self.rect.move_ip(self.shot_pos.left - 25, self.shot_pos.top -30)
                self.image_num += 1
            elif self.burning_count <= 100:
                text = "img/fire{}.png"
                self.image = pygame.image.load(text.format(self.image_num)).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (100,110))
                self.image_num += 1
                if self.image_num == 6:
                    self.image_num = 1

                collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
                if collide_list:
                    for machine in collide_list:  
                        machine.hit(0.1, lasting=True)

        self.rect.move_ip(self.dx, self.dy)
        self.burning_count += 1

class Meteorite(Bullet):

    def __init__(self, x, y, dx, dy, machines):
        """引数は初期位置(x, y)、移動量(dx, dy)、弾の当たり判定を行う対象の機体グループ"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(self.img_path+"meteorite.png").convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()   # 画像からrectを読み取る
        self.rect.move_ip(x, y)             # 引数で指定された位置に移動させる
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines        # 
        
        self.update = self.move         # updateで呼ばれるメソッドをmoveに設定する。
        self.count = 0                  # 壁に反射した回数を保存
