import pygame
import numpy as np

TRANSPARENT = (0, 0, 0, 0)
RED = (255, 0, 0)


class Sprite:

    SPRITE_SIZE: np.ndarray = np.array([25, 25])

    MAX_VELOCITY: float = 3.45
    MIN_VELOCITY: float = -1.92

    ACTION_SPACE_COUNT = 2
    MOTION_SPACE_COUNT = 2
    STEERING_SPACE_COUNT = 2

    acceleration: float = 0.025
    steering: float = 0.037
    attenuation: float = 0.25

    static_params: dict = {
        "acc_max": MAX_VELOCITY,
        "acc_min": MIN_VELOCITY,
        "acc_amount": acceleration,
        "steering_amount": steering
    }

    def __init__(self, position, rotation, offset):
        self.position = position
        self.rotation = rotation
        self.offset = offset
        self.velocity = 0.

    def initialize(self):
        # Car texture
        self.car_tex = pygame.image.load("./assets/car.png")
        self.car_tex = pygame.transform.scale(self.car_tex, Sprite.SPRITE_SIZE)
        self.car_tex.set_colorkey(TRANSPARENT)
        self.car_size = np.array(self.car_tex.get_rect().size)
        self.car_size_offset = self.car_size / 2

    def movement(self, acceleration):
        self.velocity += acceleration

        if self.velocity > Sprite.MAX_VELOCITY:
            self.velocity = Sprite.MAX_VELOCITY
        elif self.velocity < Sprite.MIN_VELOCITY:
            self.velocity = Sprite.MIN_VELOCITY

    def act(self, scaling = 1.0):
        direction = np.array([np.cos(self.rotation), -np.sin(self.rotation)])

        self.position += direction * self.velocity * scaling

    def act_actions(self, action):
        if action is None:
            return None

        motion, steering = 0., 0.
        if action in [0, 4, 5]:
            motion += Sprite.acceleration

        if action in [1, 6, 7]:
            motion -= Sprite.acceleration

        if action in [3, 5, 7]:
            steering -= Sprite.steering

        if action in [2, 4, 6]:
            steering += Sprite.steering

        self.movement(motion)
        self.rotation += steering

    def reset(self):
        self.velocity = 0.
        self.rotation = 0.

    def get_position(self):
        return self.position + self.offset - self.car_size_offset

    def render(self, screen):
        surf = pygame.transform.rotate(self.car_tex, (np.pi / 2.0) / np.pi * 180 + self.rotation / np.pi * 180)

        screen.blit(surf, self.position + self.offset - self.car_size_offset)

    def get_params(self):
        params = Sprite.static_params.copy()
        params.update({
            "pos": self.get_position(),
            "acc": self.velocity,
            "rot": self.rotation
        })

        return params
