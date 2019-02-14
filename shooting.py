#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from playermachine import PlayerMachine
from cpumachine import CpuMachine
from bullet import Bullet

class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()
        self.group = pygame.sprite.RenderUpdates()
        #self.bullets = pygame.sprite.Group()
        PlayerMachine.containers = self.group
        CpuMachine.containers = self.group
        Bullet.containers = self.group
        self.screen = pygame.display.set_mode((960, 600))
        self.player = PlayerMachine(100, 300)
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.cpumachines = [CpuMachine(900, 300), CpuMachine(900, 400), CpuMachine(900, 100)]

    def do(self):
        # メインループ
        while True:
            self.clock.tick(30)
            isClose = self.process()
            self.draw()
            if isClose:
                break
        pygame.quit()
        sys.exit()

    def process(self):
        # 1フレームごとの処理
        self.player.move(600, 960)
        self.group.update()
        for bullet in self.bullets:
            for machine in self.cpumachines:
                if machine.isHit(bullet.getHitJudge()):
                    self.group.remove(machine)
                    self.group.remove(bullet)

        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                bullet = self.player.shoot(event.key)
                if bullet:
                    self.bullets.append(bullet)
        return False

    def draw(self):
        # 描画処理
        # 画面を白に塗りつぶし
        pygame.display.update()
        self.screen.fill((255, 255, 255))
        self.group.draw(self.screen)

if __name__=='__main__':
    game = Main()
    game.do()