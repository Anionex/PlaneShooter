from entities import base
from entities import bullet
from random import randint
import pygame as pg


class MyPlane(base.Base):
    invincible_time = 2000
    shoot_cooldown = 350
    def __init__(self, *groups):
        super().__init__(*groups)
        # 上次射击时间,用于控制冷却
        self.last_shoot_time = 0
        # 控制无敌时间，用于控制无敌时间
        self.last_hit_time = 0

    def set_invincible_time(self, time):
        """
        设置无敌时间，默认为2s
        :param time:
        :return:
        """
        self.invincible_time = time

    def set_shoot_cooldown(self, time):
        """
        设置冷却时间，默认为350ms
        :param time:
        :return:
        """
        self.shoot_cooldown = time

    def shoot(self, *groups):
        """
        射出子弹\n
        :param groups:一个或多个精灵组
        :return: None
        """

        if not self.alive():
            return
        if pg.time.get_ticks() - self.last_shoot_time > self.shoot_cooldown:
            self.last_shoot_time = pg.time.get_ticks()
            new_bullet = bullet.MyBullet("assets/shot.wav", *groups)
            new_bullet.set_image("assets/bullet.png", 10, 10)
            new_bullet.set_pos(self.get_pos().x + self.rect.width / 2, self.get_pos().y)
            new_bullet.set_screen(self.screen)

    def hit(self):
        """
        如果不在无敌时间内，则收到1伤害

        """
        if pg.time.get_ticks() - self.last_hit_time > self.invincible_time:
            self.hp -= 1
            self.last_hit_time = pg.time.get_ticks()




class Enemy(base.Base):
    def __init__(self, *groups):
        super().__init__(*groups)

    def get_on_pos(self, screen):
        """
        让enemy随机在顶部随机位置出现
        :param screen:
        :return:
        """
        std_x = screen.get_width() / 2
        std_y = 0 + self.rect.height
        self.set_pos(std_x + randint(-screen.get_width() / 2 + self.rect.width / 2,
                                     + screen.get_width() / 2 - self.rect.width / 2), std_y)

    def rand_speed(self, x, rand_method):
        # 用户自定义随机函数rand_method
        self.speed = int(rand_method(x))

    def update(self, dt):
        self.move(0, self.speed * dt)

    @staticmethod
    def get_spawn_delay(my_method):
        return my_method(pg.time.get_ticks())

    @staticmethod
    def get_spawn_number(my_method):
        """
        返回基于游戏时间，下一波出现的敌人数量
        :param my_method: 自定义敌人数量和游戏时间的关系
        :return: int
        """
        return my_method(pg.time.get_ticks())


