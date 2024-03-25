import pygame
import entities
import random
import math
import pygame as pg
from constants import *

global dt

"""
需求：
1.飞机， 可上下左右移动，发射子弹 ✓
    封装在entities.plane.MyPlane类里面
2.敌机， 移动轨迹从上往下随机(？)✓， 数量速度随时间节点变化 ✓
"""

import ctypes
import sys


def is_chinese_input_method():
    # 检查平台
    if sys.platform.startswith('win'):
        try:
            # 加载user32.dll
            user32 = ctypes.windll.LoadLibrary("user32.dll")

            # 调用GetKeyboardLayout函数获取当前键盘布局
            layout = user32.GetKeyboardLayout(0)

            # 提取低16位以获得主要语言标识符
            lang_id = layout & 0xFFFF

            # 检查语言标识符是否为中文
            return lang_id == 0x0804  # 0x0804表示中文(简体)
        except Exception as e:
            print("Error:", e)
            return False
    else:
        # 非Windows系统，暂时无法检测输入法状态
        print("This feature is only supported on Windows.")
        return False


# 测试函数
def switch_to_english_input():
    # 检查平台
    if sys.platform.startswith('win'):
        try:
            # 加载user32.dll
            user32 = ctypes.windll.LoadLibrary("user32.dll")

            # 切换输入法至英文（美国）布局（0x0409）
            user32.ActivateKeyboardLayout(0x0409, 0)
            print("已切换至英文输入法")
        except Exception as e:
            print("Error:", e)
    else:
        # 非Windows系统，暂时无法切换输入法
        print("This feature is only supported on Windows.")





def my_rand_method(x):
    # 自定义随机方法，x是游戏时间戳(ms)
    return random.randint(200, int(math.log(x, 2) * 20))


def my_spawn_delay_method(x):
    return int(math.log(x, 2)) * 200


def my_spawn_number_method(x):
    return int(math.log(x / 2500))


def main():
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Plane-shooting")
    pg.display.set_icon(pg.image.load("assets/icon.png"))

    # 创建精灵组
    bullets = pg.sprite.Group()
    enemies = pg.sprite.Group()
    # all精灵组用于方便更新和绘制操作
    all = pg.sprite.Group()

    # 初始化玩家飞机，加入到对应的精灵组
    my_plane = entities.MyPlane(all)
    my_plane.set_screen(screen)
    my_plane.set_image("assets/plane.png", *PLAYER_SIZE)
    my_plane.set_pos(screen.get_width() / 2, screen.get_height() - my_plane.rect.height)

    clock = pg.time.Clock()

    # 创建用户事件，每隔一段时间就触发敌人出现
    ENEMY_SPAWN = pg.USEREVENT + 1
    spawn_delay = random.randint(MIN_SPAWN_TIME, MAX_SPAWN_TIME)
    pg.time.set_timer(ENEMY_SPAWN, spawn_delay)

    # 初始化字体对象，渲染文字
    f = pg.font.SysFont('TimesNewRoman', 50)
    f.set_bold(True)
    words = f.render("hp", False, (0, 0, 0))
    wor_rect = words.get_rect()

    score = 0
    global dt
    dt = 0

    # for i in range(5):
    #     my_plane.move(10, 10)

    # 测试函数
    if is_chinese_input_method():
        print("当前输入法为中文输入法")
        switch_to_english_input()
    else:
        print("当前输入法不是中文输入法或无法确定")
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_SPAWN:
                num = entities.Enemy.get_spawn_number(my_spawn_number_method)
                for _ in range(num):
                    new_enemy = entities.Enemy(all, enemies)
                    new_enemy.set_screen(screen)
                    new_enemy.rand_speed(pg.time.get_ticks(), my_rand_method)
                    new_enemy.set_image("assets/enemy.png", *ENEMY_SIZE)
                    new_enemy.get_on_pos(screen)

                spawn_delay = entities.Enemy.get_spawn_delay(my_spawn_delay_method)
                pg.time.set_timer(ENEMY_SPAWN, spawn_delay)

        # 键盘侦测部分
        keys = pg.key.get_pressed()
        my_plane.move(-my_plane.speed * dt * (keys[pg.K_a] - keys[pg.K_d]),
                      -my_plane.speed * dt * (keys[pg.K_w] - keys[pg.K_s]))

        # print((keys[pg.K_a] - keys[pg.K_d]), (keys[pg.K_w] - keys[pg.K_s]))
        # print(keys[pg.K_a], keys[pg.K_w])

        if keys[pg.K_SPACE]:
            my_plane.shoot(all, bullets)

        # 子弹和敌人更新，dt是时间差
        all.update(dt)

        for enemy in enemies:
            # 玩家装到敌方
            if pg.sprite.collide_mask(enemy, my_plane):
                enemy.kill()
                my_plane.hit()
                (pg.mixer.Sound("assets/crash.mpeg")).play()
            # 子弹打到敌方
            if bullet := pg.sprite.spritecollideany(enemy, bullets, pg.sprite.collide_mask):
                enemy.kill()
                bullet.kill()
                (pg.mixer.Sound("assets/score.mpeg")).play()
                score += 1
            # 敌方撞到底线
            if enemy.rect.y > SCREEN_HEIGHT:
                my_plane.hp -= 1
                enemy.kill()
                (pg.mixer.Sound("assets/crash.mpeg")).play()

        for bullet in bullets:
            if bullet.rect.y < 0:
                bullet.kill()

        if my_plane.hp <= 0:
            all.empty()
            words = f.render("GAME OVER ", True, (0, 0, 0))
            words_rect = words.get_rect()
            words_rect.center = screen.get_rect().center
            screen.blit(words, words_rect)

        all.draw(screen)
        pg.display.flip()
        dt = clock.tick(FRAMERATE) / 1000
        screen.fill("white")
        screen.blit(f.render("HP:" + str(max(0, my_plane.hp)) + "  Score:" + str(score) , False, (0, 0, 0)), wor_rect)


if __name__ == "__main__":
    main()
    pg.quit()
