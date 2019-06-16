#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
from define import R_time

class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, machines, principal, img):
        """Beamの基礎情報"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(img).convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()                     #画像大きさをrectに入れる
        self.principal = principal                            #打ったマシンの情報
        self.rect.move_ip(x, y)                               #beamの初期位置に移動
        self.dx, self.dy = dx, dy                             # 移動量
        self.machines = machines                              #相手のマシンの情報を入力
        self.gun_start = R_time.get_ticks()              #Beamを呼び足した時のクロック数を入力
        self.count = 0
        self.flag = 0                                         #画像を変化させるためのflag
        
class Beam_principal(Beam):
    def __init__(self, x, y, dx, dy, machines, principal, img):
        super().__init__(x, y, dx, dy, machines, principal,img)
        Beam_sub(x, y, dx, dy, machines, principal,"img/beam5.png")                    #beam本体に付属するエフェクトを呼び出す
        self.image = pygame.transform.smoothscale(self.image, (10,self.rect.height))   #beam本体の画像の大きさを変更
        self.rect = self.image.get_rect()                                              #大きさ変更後のrect値を格納
        x = x - self.rect.width                                                        #beam右端の値を入力
    
    def update(self):

        if self.principal.survival_flag == 1:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width,self.rect.height-1))   #本体画像の高さを-1する
            self.rect = self.image.get_rect()                                                             #画像の高さが変わるのでrect値を更新

            #クロック数が1000以上とbeam本体の横の長さが600以下
        if R_time.get_ticks() - self.gun_start >= 1000 and self.rect.width <= 600 and self.principal.survival_flag == 0:                   
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width+10,self.rect.height))  #画像の大きさを横に10に長くする
            self.rect = self.image.get_rect()                                                             #画像の長さが変わるのでrect値を更新
        elif self.rect.width >= 600 and self.count == 0:                                                  #本体の長さが600以上とこの行のelifが呼び出されたことがないこと
            self.gun_start = R_time.get_ticks()                                                      #本体が伸び切った時のクロック数を入力
            self.flag = 1                                                                                 #次の段階に進むためのフラッグを１入力
            self.count = 1 
            
            #本体が伸び切ってからのクロック数が1000以上と本体の高さが０より大きいとflagが１であること
        if R_time.get_ticks() - self.gun_start >= 1000 and self.rect.height > 0 and self.flag == 1 and self.principal.survival_flag == 0:  
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width,self.rect.height-1))   #本体画像の高さを-1する
            self.rect = self.image.get_rect()                                                             #画像の高さが変わるのでrect値を更新
        elif self.rect.height == 0:                                                                       #本体の高さが0であること
            self.kill()                                                                                   #本体のspriteを削除する
            
        #ここのコードでbeam本体をmachineに追従させる
        x, y = self.principal.rect.midleft                                                                #打ったmachineの座標を所得する
        self.rect.midright = (x, y+5)                                                                     #beam本体の座標を打ったmachineの座標に合わせる
        
        collide_list = pygame.sprite.spritecollide(self, self.machines, False)      # グループmachinesからこの弾に当たったスプライトをリストでとる
        if collide_list:                                                            # リストがあるか
            for machine in collide_list:                                           # この弾に当たったすべての機体に対してダメージを与える
                machine.hit(.1)
            
class Beam_sub(Beam):  #サブクラス
    def __init__(self, x, y, dx, dy, machines, principal,img):
        super().__init__(x, y, dx, dy, machines, principal, img)                    #superクラス(beam)から呼び出す
        self.change_image = pygame.image.load("img/beam5.png").convert_alpha()      #サブ用の画像を呼び込む
        self.image = pygame.transform.smoothscale(self.image, (9,6))                #それそれの大きさの画像を設定する
        self.c_image1 = pygame.transform.smoothscale(self.image, (14,9))
        self.c_image2 = pygame.transform.smoothscale(self.image, (17,12))
        self.c_image3 = pygame.transform.smoothscale(self.image, (20,15))
        self.c_image4 = pygame.transform.smoothscale(self.image, (23,18))
        self.c_image5 = pygame.transform.smoothscale(self.image, (25,23))
        self.c_image9 = pygame.transform.smoothscale(self.change_image, (27,24))
        self.c_data = [self.c_image1,self.c_image2,self.c_image3,self.c_image4,self.c_image5,self.c_image9] #データを配列に格納する
        
        #ここでサブ画像の大きさを大きくする
    def update(self):
        if  self.principal.survival_flag == 1:                                                            #このフラッグが１の時マシンは消滅している
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width-1,self.rect.height-1)) #サブ画像の縦横をそれぞれ-1する
            self.rect = self.image.get_rect()                                                             #画像の大きさが変わるのでrect値を更新

        if  self.flag == 0 and self.count < 6 and self.principal.survival_flag == 0:    #格納したデータを置き換えながら表示する
            self.image = self.c_data[self.count]
            self.rect = self.image.get_rect() 
            self.count += 1
        elif self.count < 7:
            self.flag = 1 
            
            #ここでサブ画像を小さくする
            #呼び出されてからのクロックすうが3900以上　サブ画像の高さが０よ大きい　flagが１であること

        if R_time.get_ticks() - self.gun_start >= 3900 and self.flag == 1 and self.rect.height > 0 and self.principal.survival_flag == 0:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width-1,self.rect.height-1)) #サブ画像の縦横をそれぞれ-1する
            self.rect = self.image.get_rect()                                                             #画像の大きさが変わるのでrect値を更新
        elif self.rect.height == 0:                                                                       #サブ画像の高さが0であること
            self.kill()                                                                                   #サブ画像のspriteを削除する
            self.principal.beam_flag = 0
            
        #ここのコードでbeamサブをmachineに追従させる
        x, y = self.principal.rect.midleft                                                                        #打ったmachineの座標を所得する
        self.rect.midright = (x, y+5)                                                                     #beam本体の座標を打ったmachineの座標に合わせる
        
