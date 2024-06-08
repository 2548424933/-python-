import pygame
from pygame import *      # * 表示引入所有方法 如 pygame.K_a
import time


#飞机类
class HeroPlane():
    def __init__(self,screen):
        #4创建玩家飞机
        self.player = pygame.image.load('./image/me1.png')
        #飞机初始位置
        self.x = 189
        self.y = 500
        #飞机速度
        self.speed = 2
        self.screen = screen
        # 转子弹的列表
        self.bullets = []

    def key_control(self):
        # 监听键盘事件
        key_presed = pygame.key.get_pressed()  # get_pressed是按的意思
        if key_presed[K_w] or key_presed[K_UP]:
            self.y -= self.speed
        if key_presed[K_s] or key_presed[K_DOWN]:
            self.y += self.speed
        if key_presed[K_a] or key_presed[K_LEFT]:
            self.x -= self.speed
        if key_presed[K_d] or key_presed[K_RIGHT]:
            self.x += self.speed
        if key_presed[K_SPACE]:
            if key_presed[K_SPACE]:
                bullet = Bullet(self.screen, self.x+51, self.y)
                self.bullets.append(bullet)

    def display(self):
        # 将飞机图片贴到窗口中
        self.screen.blit(self.player, (self.x, self.y))            #注意screen是窗口，不是背景！！！！！！！是在窗口上贴上去的

        #遍历所有子弹
        for bullet in self.bullets:
            #让子弹飞起来 修改Y坐标
            bullet.auto_move()
            #子弹显示
            bullet.display()
            # self.screen.blit(bullet,(self.x,self.y))

#子弹类
class Bullet():
    def __init__(self,screen,x,y):
        self.x = x
        self.y = y
        self.bbullet = pygame.image.load('./bullet1.png')
        self.screen = screen
        self.speed = 3

    def display(self):
        self.screen.blit(self.bbullet,(self.x,self.y))

    def auto_move(self):
        self.y -= self.speed



def main():
    # 1创建一个窗口
    screen = pygame.display.set_mode((480, 700), 0, 32)  # 显示窗口、设置模式
    # 2创建一个图片
    background = pygame.image.load('./image/background.png')

    player = HeroPlane(screen)

    while True:
        # 3将背景图片贴到窗口   不断更新图片的位置
        screen.blit(background, (0, 0))  # blit 贴上去             # 后面贴上去的位置参数是需要加括号的
        #获取事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #执行pygame退出
                pygame.quit()
                #python程序退出
                exit()

        #执行飞机的安全监听
        player.key_control()

        #飞机的显示
        player.display()

        #更新需要显示的内容!!
        pygame.display.update()
        time.sleep(0.01)

import warnings
warnings.filterwarnings("ignore")

main()









# import os
# from tqdm import tqdm
# import cv2
# from skimage import io
# path = r"C:\Users\86135\重要误删PycharmProjects\pythonProject2\飞机大战\image"
# fileList = os.listdir(path)
# for i in tqdm(fileList):
#     image = io.imread(path+i)
#     image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
#     cv2.imencode('.png',image)[1].tofile(path+i)

# def key_control_2(self):
#     while True:
# screen = pygame.display.set_mode((480, 700), 0, 32)
# background = pygame.image.load('./image/background.png')
# screen.blit(background, (0, 0))
# for event in pygame.event.get():         #这个就是不连续监听了，就是按一下才会执行一下
#     if event.type == pygame.KEYDOWN:
#         if event.key == [K_SPACE]:
#             bullet = Bullet(self.screen,self.x,self.y)
#             self.bullets.append(bullet)

