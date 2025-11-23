
from __future__ import annotations

import pygame

from .entity import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Controller:
    def __init__(self, game: Game):
        self.game: Game = game

    def update(self, entity: Entity, dt: float):
        ...


class PlayerController(Controller):
    def __init__(self, game):
        super().__init__(game)
        
        self.pressed_keys = pygame.key.get_pressed()
        self.just_pressed_keys = pygame.key.get_just_pressed()
        self.just_released_keys = pygame.key.get_just_released()

        self.pressed_mouse = pygame.mouse.get_pressed()
        self.just_pressed_mouse = pygame.mouse.get_just_pressed()
        self.just_released_mouse = pygame.mouse.get_just_released()


    def get_inputs(self):
        self.pressed_keys = pygame.key.get_pressed()
        self.just_pressed_keys = pygame.key.get_just_pressed()
        self.just_released_keys = pygame.key.get_just_released()

        self.pressed_mouse = pygame.mouse.get_pressed()
        self.just_pressed_mouse = pygame.mouse.get_just_pressed()
        self.just_released_mouse = pygame.mouse.get_just_released()


    def update(self, entity, dt):
        self.get_inputs()
        entity.inputs = {
            "up": self.pressed_keys[pygame.K_w],
            "down": self.pressed_keys[pygame.K_s],
            "left": self.pressed_keys[pygame.K_a],
            "right": self.pressed_keys[pygame.K_d],
            "attack": self.just_pressed_mouse[0]
        }

        return super().update(entity, dt)


import random

class RandomController(Controller):
    def __init__(self, game):
        super().__init__(game)
        # self.active_time = 0

    def update(self, entity, dt):
        # if not self.active_time:
        #     return
        # entity.inputs = {
        #     "up": random.choice([False, True]),
        #     "down": random.choice([False, True]),
        #     "left": random.choice([False, True]),
        #     "right": random.choice([False, True]),
        #     "attack": False
        # }
        return super().update(entity, dt)

