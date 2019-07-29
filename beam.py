#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
from define import R_time
from timer import *

class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        """Beamの基礎情報"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(img).convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()                     #画像大きさをrectに入れる
        self.rect.move_ip(x, y)                               #beamの初期位置に移動
        
class Beam_principal(Beam):
    def __init__(self, x, y, machines, principal, img, angle):
        super().__init__(x, y ,img)
        self.image = pygame.transform.rotate(self.image, angle)
        if angle == 0 or 180:
            self.image0__init__()
        elif angle == 90 or 270:
            self.image90__init__()
        #self.length_select(angle)
        self.image = self.p_image1
        self.rect.left =- self.rect.width                                                        #beam右端の値を入力
        self.rect = self.image.get_rect()                                              #大きさ変更後のrect値を格納
        self.alpha_flag = True
        self.kill_flag = False
        self.alpha_time = Timer(1200,self.Change_flag, 0, None)
        self.kill_time = None
        self.principal = principal 
        self.machines = machines
        self.lord_sub = True
        self.angle = angle
        
    
    def update(self):

        if self.principal.survival_flag == 1:
            self.kill_flag = True
            if self.alpha_flag != None:
                self.aplha_flag = None
            if self.alpha_time != None:
                self.alpha_time.kill()
            if self.kill_time != None:
                self.kill_time.kill()

            #クロック数が1000以上とbeam本体の横の長さが600以下
        if self.principal.survival_flag == 0 and self.alpha_flag: 
            self.image = self.p_image2
            self.Change_flag(0, False)
        elif self.principal.survival_flag == 0 and self.alpha_flag == False:
            if self.rect.width <= 600 and self.angle == 0 or 180:
                self.rect.width += 80    
            elif self.rect.height <= 250 and self.angle == 90 or 270:
                self.rect.height += 40
            self.p_image1 = pygame.transform.smoothscale(self.p_image1, (self.rect.width,self.rect.height))
            self.p_image2 = pygame.transform.smoothscale(self.p_image2, (self.rect.width,self.rect.height))
            self.image = self.p_image1
            self.Change_flag(0, True)
        
        if self.principal.survival_flag == 0 and self.alpha_flag == None and self.image_number != 6:
            self.image = self.image_list[self.image_number]
            self.rect = self.image.get_rect()
            self.image_number += 1
            if self.image_number == 6:
                self.kill_time = Timer(2000, self.Change_flag, 1, True)
            
            #本体が伸び切ってからのクロック数が1000以上と本体の高さが０より大きいとflagが１であること
        if self.rect.height > 0 and self.kill_flag and self.angle == 0 or 180:  
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width,self.rect.height-1))   #本体画像の高さを-1する
            self.rect = self.image.get_rect()                                                             #画像の高さが変わるのでrect値を更新
        elif self.rect.width > 0 and self.kill_flag and self.angle == 90 or 270:  
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width-1,self.rect.height))   #本体画像の高さを-1する
            self.rect = self.image.get_rect()
        elif self.rect.height == 0 or self.rect.width == 0:                                              #本体の高さが0であること
            self.kill()                                                                                  #本体のspriteを削除する
            Timer(500,self.Change_flag, 2, 0)
        
        x,y = self.principal.rect.midright
        if self.alpha_flag == None and self.principal.cop_flag and self.lord_sub:
            Beam_sub(x, y, self, "img/beam6.png")
            self.lord_sub = False
        elif self.alpha_flag == None and self.principal.cop_flag == False and self.lord_sub:
            Beam_sub(x, y, self, "img/beam5.png")
            self.lord_sub = False

        #ここのコードでbeam本体をmachineに追従させる
        if self.angle == 0:
            self.rect.midleft = (x-self.principal.rect.width, y+5)
        elif self.angle == 90:
            self.rect.midtop = (x-self.principal.rect.width, self.principal.rect.bottom)                                       #beam本体の座標を打ったmachineの座標に合わせる
        
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list and self.alpha_flag == None:                                # リストがあるか
            for machine in collide_list:                                            # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(0.1, lasting=True)
            
        print(self.rect.width)
        print(self.kill_flag)
        
    def Change_flag(self, number, boolean):
        if number == 0:
            self.alpha_flag = boolean
        if number == 1:
            self.kill_flag = boolean
        if number == 2:
            self.principal.bema_flag = boolean 
    
    def image0__init__(self):
        self.p_image1 = pygame.transform.smoothscale(self.image,(5,2))
        self.p_image2 = self.p_image1.copy()
        self.p_image2.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
        self.p_image3 = pygame.transform.smoothscale(self.image, (645,3))
        self.p_image4 = pygame.transform.smoothscale(self.image, (645,4))
        self.p_image5 = pygame.transform.smoothscale(self.image, (645,5))
        self.p_image6 = pygame.transform.smoothscale(self.image, (645,6))
        self.p_image7 = pygame.transform.smoothscale(self.image, (645,7))
        self.p_image8 = pygame.transform.smoothscale(self.image, (645,9))
        self.image_list = [self.p_image3, self.p_image4, self.p_image5,self.p_image6, self.p_image7, self.p_image8]
        self.image_number = 0
    
    def image90__init__(self):
        self.p_image1 = pygame.transform.smoothscale(self.image,(2,5))
        self.p_image2 = self.p_image1.copy()
        self.p_image2.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
        self.p_image3 = pygame.transform.smoothscale(self.image, (3,250))
        self.p_image4 = pygame.transform.smoothscale(self.image, (4,250))
        self.p_image5 = pygame.transform.smoothscale(self.image, (5,250))
        self.p_image6 = pygame.transform.smoothscale(self.image, (6,250))
        self.p_image7 = pygame.transform.smoothscale(self.image, (7,250))
        self.p_image8 = pygame.transform.smoothscale(self.image, (9,250))
        self.image_list = [self.p_image3, self.p_image4, self.p_image5,self.p_image6, self.p_image7, self.p_image8]
        self.image_number = 0
    
    def length_select(self,angle):
        if angle == 0 or 180:
            self.beam_length =  600
        elif angle == 90 or 270:
            self.beam_length =  100

class Beam_sub(Beam):  #サブクラス
    def __init__(self, x, y, principal, img):
        super().__init__(x, y, img)                    #superクラス(beam)から呼び出す
        self.image = pygame.transform.rotate(self.image, principal.angle)
        self.image__init__()
        self.principal = principal
        self.count = 0
        
        #ここでサブ画像の大きさを大きくする
    def update(self):
        if  self.principal.kill_flag:                                                                                  #このフラッグが１の時マシンは消滅している
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width-2,self.rect.height-2)) #サブ画像の縦横をそれぞれ-1する
            self.rect = self.image.get_rect()                                                             #画像の大きさが変わるのでrect値を更新
            if self.rect.height <= 0:
                self.kill()

        if  self.count < 6:                                  #格納したデータを置き換えながら表示する
            self.image = self.c_data[self.count]
            self.rect = self.image.get_rect() 
            self.count += 1
        
        if self.principal.angle == 0:
            x,y = self.principal.principal.rect.left,self.principal.rect.centery
            self.rect.midright = (x, y)
        elif self.principal.angle == 90:
            x,y = self.principal.principal.rect.centerx,self.principal.rect.bottom
            self.rect.centerx,self.rect.top = (x, y+7)
        elif self.principal.angle == 180:
            x,y = self.principal.principal.rect.right,self.principal.rect.centery
            self.rect.midleft = (x, y)
        elif self.principal.angle == 270:
            x,y = self.principal.principal.rect.centerx,self.principal.rect.top
            self.rect.centerx,self.rect.bottom = (x, y-7)

    def image__init__(self):
        self.copy_image = self.image.copy()
        self.image = pygame.transform.smoothscale(self.copy_image, (9,6))                #それそれの大きさの画像を設定する
        self.c_image0 = pygame.transform.smoothscale(self.copy_image, (14,9))
        self.c_image1 = pygame.transform.smoothscale(self.copy_image, (17,12))
        self.c_image2 = pygame.transform.smoothscale(self.copy_image, (20,15))
        self.c_image3 = pygame.transform.smoothscale(self.copy_image, (23,18))
        self.c_image4 = pygame.transform.smoothscale(self.copy_image, (25,23))
        self.c_image5 = pygame.transform.smoothscale(self.copy_image, (27,24))
        self.c_data = [self.c_image0,self.c_image1,self.c_image2,self.c_image3,self.c_image4,self.c_image5] #データを配列に格納す
