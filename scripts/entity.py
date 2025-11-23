from __future__ import annotations

import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Entity:
    def __init__(self, game: Game, pos: pygame.Vector2 = pygame.Vector2()):
        self.game: Game = game

        self.pos: pygame.Vector2 = pos
        self.vel: pygame.Vector2 = pygame.Vector2()
        self.acc: pygame.Vector2 = pygame.Vector2()
    

    def update(self, dt: float):
        self.pos += self.vel*dt
        self.vel += self.acc*dt

