import pygame
from pygame import  *      # * 表示引入所有方法 如 pygame.K_a
from pygame import time
import time
clock = pygame.time.Clock
def main():
    # 1穿件一个窗口
    screen = pygame.display.set_mode((480,700),0,32)         #显示窗口、设置模式
    # 2创建一个图片
    background = pygame.image.load('./image/background.png')
    # 2创建一个玩家飞机图片
    player = pygame.image.load('./image/me1.png')

    # 4显示窗口的内容
    pygame.display.update()  # 显示
    x = 189
    y = 500
    while True:
        # clock.tick(1)
        # 3将背景图片贴到窗口   不断更新图片的位置
        screen.blit(background, (0, 0))  # blit 贴上去
        screen.blit(player, (x, y))
        #获取事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #执行pygame退出
                pygame.quit()
                #python程序退出
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    print('空格')

        #更新需要显示的内容
        pygame.display.update()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
