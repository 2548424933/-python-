import random
import pygame
from pygame import *      # * 表示引入所有方法 如 pygame.K_a
import time

#玩家飞机类
class HeroPlane(pygame.sprite.Sprite):
    bullets = pygame.sprite.Group()
    #用作碰撞判断（存放所有飞机子弹的组）289
    def __init__(self,screen):
        #这个精灵的初始化方法 必须调用
        pygame.sprite.Sprite.__init__(self)

        #4创建玩家飞机
        self.image = pygame.image.load('./image/me1.png')           #名字必须是image

        #精灵根据图片image获取举行对象
        self.rect = self.image.get_rect()   #rect:矩形  ！！.image.get_rect获得图片,但是现在只能知道宽高，还不能确定位置
        self.rect.topleft = [189,500]       #设置初始位置      189,500

        #飞机速度
        self.speed = 4
        self.screen = screen
        # 装子弹的列表
        self.bullets = pygame.sprite.Group()           #！！Group是专门用来装精灵的，类似列表  添加add   遍历添加draw 后面会用到
        # self.bullet = []
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
                bullet = Bullet(self.screen, self.rect.left+51, self.rect.top)     #rect.left表示矩形飞机的左上角
                self.bullets.add(bullet)
                # self.bullet.append(bullet)
                HeroPlane.bullets.add(bullet)

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
    bullets = pygame.sprite.Group()
    def __init__(self,screen):
        #精灵的初始化方法
        pygame.sprite.Sprite.__init__(self)
        #4创建玩家飞机
        self.image = pygame.image.load('./image/enemy1.png')
        #飞机初始位置
        self.rect = self.image.get_rect()
        x = random.randrange(0,Manager.by_size[0],50)
        self.rect.topleft = [x,0]
        #飞机速度
        self.speed = 1
        self.screen = screen
        # 转子弹的列表
        self.bullets = pygame.sprite.Group()
        #  初始运动方向
        self.direction = "right"
        # self.ebullet = []
    def auto_move(self):
        if self.direction == 'right':
            self.rect.left += self.speed
        elif self.direction == 'left':
            self.rect.left -= self.speed

        if self.rect.right > 480:
            self.direction = 'left'
        elif self.rect.left < 0:
            self.direction = 'right'
        self.rect.bottom += 2   #直线运动

    def display(self):
        # 将飞机图片贴到窗口中
        self.screen.blit(self.image,self.rect)
        self.bullets.update()
        self.bullets.draw(self.screen)

    def auto_fire(self):
        #降低子弹频率
        random_num = random.randint(1,50)
        if random_num == 8:
            #将子弹储存在一个列表
            bullet = EnemyBullet(self.screen,self.rect.left+28,self.rect.top+43)
            self.bullets.add(bullet)
            EnemyPlane.bullets.add(bullet)
            # self.ebullet.append(bullet)

    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()

#子弹类
class Bullet(pygame.sprite.Sprite):
    # bullets = pygame.sprite.Group()  # 这样子可以在289直接调用HeroPlane.bullets
    def __init__(self,screen,x,y):
        # 精灵类初始化
        pygame.sprite.Sprite.__init__(self)
        #创建图片
        self.image = pygame.image.load('./image/bullet1.png')
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
        # for i in P:
        #     Bullet.bullets.add(i)


class EnemyBullet(pygame.sprite.Sprite):
    # bullets = pygame.sprite.Group()
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
        # for i in p:
        #     EnemyBullet.bullets.add(i)

class Bomb():
    def __init__(self,screen,type):
        self.screen = screen
        if type == 'enemy':
            #加载爆炸资源
            self.mImage = [pygame.image.load('./image/enemy1_down' + str(v) + '.png') for v in range(1,5)]
        elif type == 'player':
            self.mImage = [pygame.image.load('./image/me_destroy_' + str(v) + '.png') for v in range(1,5)]
        #设置当前爆炸播放索引
        self.mIndex = 0
        # 爆炸设置 坐标位置
        self.mPos = [0,0]
        # 是否可见
        self.mVisible = False

    def action(self,rect):    #rect位置
        #触发爆炸方法draw
        #爆炸的坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        #打开爆炸特效
        self.mVisible = True

    def draw(self):
        if self.mVisible == False:
            return
        else:
            self.screen.blit(self.mImage[self.mIndex],(self.mPos[0],self.mPos[1]))
            self.mIndex += 1                      #不需要while，因为在self.mVisible = False之前，整个方法不会结束，一直在执行
            if self.mIndex >= len(self.mImage):
                #如果小标已经到最后了 代表爆炸结束
                #下标位置重置 mVisible重置
                self.mIndex = 0
                self.mVisible = False


#音乐
class GameSound():
    def __init__(self):
        pygame.mixer.init()          # 音乐模块初始化
        pygame.mixer.music.load('./image/全民飞机大战音效 (664)_爱给网_aigei_com.mp3')
        pygame.mixer.music.set_volume(0.2)  #音量大小

        self._bomb = pygame.mixer.Sound('./image/bomb.mp3')
    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)          #-1表示循环播放

    def playBombSound(self):
        pygame.mixer.Sound.play(self._bomb)      #带self会有点特殊，调用时只会显示一次


#地图移动
class GameBackground():
    def __init__(self,screen):
        self.mImage1 = pygame.image.load('./image/background.png')
        self.mImage2 = pygame.image.load('./image/background.png')
        self.screen = screen
        self.y1 = 0
        self.y2 = -Manager.by_size[1]

    def move(self):
        self.y1 += 2
        self.y2 += 2
        if self.y1 == Manager.by_size[1]:
            self.y1 = 0
        if self.y2 == 0:
            self.y2 = -Manager.by_size[1]

    def draw(self):
        self.move()       #调用上面方法
        self.screen.blit(self.mImage1,(0,self.y1))
        self.screen.blit(self.mImage2,(0,self.y2))


class Manager():
    by_size = (480,700)
    # 游戏结束 倒计时
    game_over_id = 11
    # 游戏是否结束
    is_game_over = False
    #创建敌机定时器id
    create_enemy_id = 10
    #

    def __init__(self):
        #创建窗口
        self.screen= pygame.display.set_mode((480,700),0,32)
        #创建背景图片
        self.background = pygame.image.load('./image/background.png')
        #初始化一个装玩家精灵的group
        self.players = pygame.sprite.Group()
        #初始化一个装敌机精灵的group
        self.enemys = pygame.sprite.Group()
        # #初始化一个玩家爆炸的对象
        self.player_bomb = Bomb(self.screen,'player')
        # #初始化一个敌机爆炸的对象
        self.enemy_bomb = Bomb(self.screen,'enemy')
        #
        self.player_bullet_bomb = Bomb(self.screen,'player_bullet')
        #初始化一个声音播放的对象
        self.sound = GameSound()
        #玩家子弹
        self.player_bullet = pygame.sprite.Group()
        #背景图
        self.map = GameBackground(self.screen)


    def exit(self):
        print('退出')
        pygame.quit()
        exit()

    def new_player(self):                                      #!这里想创建几个对象就定义几个方法
        #创建飞机对象 添加到玩家的组
        player = HeroPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        #创建敌机的对象 添加到敌机的组
        enemy = EnemyPlane(self.screen)
        self.enemys.add(enemy)

    def main(self):
        #播放背景音乐
        self.sound.playBackgroundMusic()
        #想要创建几个对象就复制几次
        #创建玩家 （调用方法）
        self.new_player()
        #开启创建敌机的定时器
        pygame.time.set_timer(Manager.create_enemy_id,5000)     #每1000毫米创建一次

        self.new_enemy()
        print(self.player_bullet)
        while True:
            #把背景图片贴到窗口
            self.map.draw()
            #遍历所有的事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                elif event.type == Manager.create_enemy_id:
                    self.new_enemy()
            #调用爆炸的对象(调用方法)
            self.player_bomb.draw()     #!其实这个方法应该放在后面的
            self.enemy_bomb.draw()

            #判断碰撞
            iscollide = pygame.sprite.groupcollide(self.players,self.enemys,True,True)  #self.players指的是所有player = HeroPlane(self.screen)精灵子对象
            if iscollide:           #如果碰撞了，iscollide返回的是这个{<HeroPlane Sprite(in 0 groups)>: [<EnemyPlane Sprite(in 0 groups)>]}
                # print(iscollide)
                items = list(iscollide.items())[0]          #使用items()方法可以将字典中的键值对以元组的形式返回
                # print(items)
                # x,y 分别代表两架飞机 HeroPlane和EnemyPlane
                x = items[0]
                # print(x)
                y = items[1][0]            #[1][0]因为后面EnemyPlane对象是个列表，不懂运行print，
                # print(y)
                # 玩家爆炸图片
                self.player_bomb.action(x.rect)
                # # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                #爆炸声音
                self.sound.playBombSound()

            #判断玩家子弹与敌机碰撞
            iscollide1 = pygame.sprite.groupcollide(HeroPlane.bullets,self.enemys,True,True)
            if iscollide1:
                items = list(iscollide1.items())[0]
                y = items[1][0]
                #敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                #爆炸声音w
                self.sound.playBombSound()
                EnemyPlane.bullets.empty()

            #判断敌机子弹与玩家碰撞
            iscollide2 = pygame.sprite.groupcollide(EnemyPlane.bullets,self.players,True,True)
            if iscollide2:
                items = list(iscollide2.items())[0]
                y = items[1][0]
                self.player_bomb.action(y.rect)
                self.sound.playBombSound()


            #玩家飞机和子弹的显示
            self.players.update()
            #敌机和子弹的显示
            self.enemys.update()
            # self.enemys.draw(self.screen)

            #刷新窗口内容
            pygame.display.update()
            time.sleep(0.01)


if __name__ == '__main__':
    manager = Manager()
    manager.main()


