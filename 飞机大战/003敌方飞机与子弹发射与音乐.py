import random

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

#敌方飞机
class   EnemyPlane():
    def __init__(self,screen):
        #4创建玩家飞机
        self.player = pygame.image.load('./image/enemy1.png')
        #飞机初始位置
        self.x = 0
        self.y = 0
        #飞机速度
        self.speed = 1
        self.screen = screen
        # 转子弹的列表
        self.bullets = []
        #  初始运动方向
        self.direction = "right"

    def auto_move(self):
        if self.direction == 'right':
            self.x += 2
        elif self.direction == 'left':
            self.x -= 2

        if self.x > 423:
            self.direction = 'left'
        elif self.x == 0:
            self.direction = 'right'

    def display(self):
        # 将飞机图片贴到窗口中
        self.screen.blit(self.player, (self.x, self.y))

    def auto_fire(self):
        #降低子弹频率
        random_num = random.randint(1,10)
        if random_num == 8:
            #将子弹储存在一个列表
            bullet = EnemyBullet(self.screen,self.x+28,self.y+43)
            self.bullets.append(bullet)
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
        self.bbullet = pygame.image.load('./image/bullet1.png')
        self.screen = screen
        self.speed = 3

    def display(self):
        self.screen.blit(self.bbullet,(self.x,self.y))

    def auto_move(self):
        # self.display()
        self.y -= self.speed


class EnemyBullet():
    def __init__(self,screen,x,y):
        self.x = x
        self.y = y
        self.bbullet = pygame.image.load('./image/bullet2.png')
        self.screen = screen
        self.speed = 3

    def display(self):
        self.screen.blit(self.bbullet,(self.x,self.y))

    def auto_move(self):
        # self.display()
        self.y += self.speed
class GameSound():
    def __init__(self):
        pygame.mixer.init()          # 音乐模块初始化
        pygame.mixer.music.load('./image/全民飞机大战音效 (664)_爱给网_aigei_com.mp3')

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)          #-1表示循环播放




def main():                             #完成整个程序的控制
    sound = GameSound()
    sound.playBackgroundMusic()

    # 1创建一个窗口
    screen = pygame.display.set_mode((480, 700), 0, 32)  # 显示窗口、设置模式
    # 2创建一个图片
    background = pygame.image.load('./image/background.png')

    #创建一个我方飞机对象
    player = HeroPlane(screen)
    #创建一个敌方飞机对象
    enemy = EnemyPlane(screen)

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

        #执行我方飞机的安全监听
        player.key_control()
        #我方飞机的显示
        player.display()

        #敌方飞机的显示和移动
        enemy.auto_move()
        enemy.display()
        #敌机自动开火
        enemy.auto_fire()


        #更新需要显示的内容!!
        pygame.display.update()
        time.sleep(0.01)

main()