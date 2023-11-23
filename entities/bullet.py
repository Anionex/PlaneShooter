import pygame.mixer

from entities import base
from pygame import mixer

class MyBullet(base.Base):

    def __init__(self, sound_src, *groups):
        super().__init__(*groups)
        gun_shot_sound = pygame.mixer.Sound(sound_src)
        gun_shot_sound.play()

    def update(self, dt):
        self.move(0, -self.speed * dt)

