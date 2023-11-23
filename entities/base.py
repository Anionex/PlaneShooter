import pygame as pg
from pygame.sprite import collide_mask
from constants import *

class Base(pg.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)  # 有问题
        self.hp = DEFAULT_HP
        self.speed = DEFAULT_SPEED
        self.rect = self.screen = self.image = None

    def set_image(self, path, width, height):
        """
        设置实体的图片
        :param path: 图片存放路径
        :param width:
        :param height:
        :return:
        """
        loaded_img = pg.image.load(path)
        self.image = pg.transform.scale(loaded_img, (width, height))
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    """
    def is_colliding(self, entities):
        ret = 0
        for entity in entities:
            if self != entity:
                ret = ret or collide_mask(self, entity)
        return ret
    """

    def set_screen(self, sc):
        """
        设置承载实体的Surface对象
        :param sc:
        :return:
        """
        self.screen = sc

    """
    def draw(self):
        if self.hp > 0:
            self.screen.blit(self.image, self.rect)
    """

    def get_pos(self):
        return self.rect

    def is_out_of_screen(self):
        return self.rect.y < 0 or self.rect.y > self.screen.get_height()
