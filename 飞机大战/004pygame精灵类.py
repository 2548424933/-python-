import random

import pygame
from pygame import *      # * 表示引入所有方法 如 pygame.K_a
import time


#飞机类
class HeroPlane(pygame.sprite.Sprite):
    def __init__(self,screen):
        #这个精灵的初始化方法 必须调用
        pygame.sprite.Sprite.__init__(self)

        #4创建玩家飞机
        self.image = pygame.image.load('./image/me1.png')

        #精灵根据图片image获取举行对象
        self.rect = self.image.get_rect()   #rect:矩形  ！！.image.get_rect获得图片,但是现在只能知道宽高，还不能确定位置
        self.rect.topleft = [189,500]       #设置初始位置      189,500

        #飞机速度
        self.speed = 2
        self.screen = screen
        # 转子弹的列表
        self.bullets = pygame.sprite.Group()           #！！Group是专门用来装精灵的，类似列表  添加add   遍历添加draw 后面会用到

    def key_control(self):
        # 监听键盘事件
        key_presed = pygame.key.get_pressed()  # get_pressed是按的意思
        if key_presed[K_w] or key_presed[K_UP]:
            self.rect.top -= self.speed
        if key_presed[K_s] or key_presed[K_DOWN]:
            self.rect.bottom += self.speed
        if key_presed[K_a] or key_presed[K_LEFT]:
            self.rect.left -= self.speed
        if key_presed[K_d] or key_presed[K_RIGHT]:
            self.rect.right += self.speed
        if key_presed[K_SPACE]:
            if key_presed[K_SPACE]:
                bullet = Bullet(self.screen, self.rect.left+51, self.rect.top)     #rect.left表示矩形飞机的左上角
                self.bullets.add(bullet)

    def display(self):
        # 将飞机图片贴到窗口中
        self.screen.blit(self.image,self.rect)            #注意screen是窗口，不是背景！！！！！！！是在窗口上贴上去的
        #调用子弹类的方法
        self.bullets.update()
        #把所有子弹全部添加到屏幕(！！！！!Group中的一种用法)，这样就不用for循环了
        self.bullets.draw(self.screen)

    def update(self):
        self.key_control()
        self.display()



#敌方飞机
class   EnemyPlane(pygame.sprite.Sprite):
    def __init__(self,screen):
        #精灵的初始化方法
        pygame.sprite.Sprite.__init__(self)
        #4创建玩家飞机
        self.image = pygame.image.load('./image/enemy1.png')
        #飞机初始位置
        self.rect = self.image.get_rect()
        self.rect.topleft = [0,0]
        #飞机速度
        self.speed = 1
        self.screen = screen
        # 转子弹的列表
        self.bullets = pygame.sprite.Group()
        #  初始运动方向
        self.direction = "right"

    def auto_move(self):
        if self.direction == 'right':
            self.rect.left += self.speed
        elif self.direction == 'left':
            self.rect.left -= self.speed

        if self.rect.right > 480:
            self.direction = 'left'
        elif self.rect.left < 0:
            self.direction = 'right'

    def display(self):
        # 将飞机图片贴到窗口中
        self.screen.blit(self.image,self.rect)
        self.bullets.update()
        self.bullets.draw(self.screen)

    def auto_fire(self):
        #降低子弹频率
        random_num = random.randint(1,10)
        if random_num == 8:
            #将子弹储存在一个列表
            bullet = EnemyBullet(self.screen,self.rect.left+28,self.rect.top+43)
            self.bullets.add(bullet)


    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()

#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        # 精灵类初始化
        pygame.sprite.Sprite.__init__(self)
        #创建图片
        self.image = pygame.image.load('./bullet1.png')
        #获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

        self.screen = screen
        self.speed = 3

    def update(self):
        #修改子弹坐标
        self.rect.top -= self.speed
        #如果子弹出界则会销毁子弹
        if self.rect.top < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./image/bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

        self.screen = screen
        self.speed = 3

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > 700:
            self.kill()

class GameSound():
    def __init__(self):
        pygame.mixer.init()          # 音乐模块初始化
        pygame.mixer.music.load('./image/全民飞机大战音效 (664)_爱给网_aigei_com.mp3')
        pygame.mixer.music.set_volume(0.02)  #音量大小

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


        #我方飞机的显示
        player.update()

        #敌方飞机的显示和移动
        enemy.update()

        #更新需要显示的内容!!
        pygame.display.update()
        time.sleep(0.01)

main()