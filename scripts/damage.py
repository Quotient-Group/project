
from __future__ import annotations

import pygame

from .entity import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class DamageHitbox(Entity):
    def __init__(self, game: Game, pos: pygame.Vector2, mask: pygame.Mask = pygame.Mask((0,0))):
        super().__init__(game, pos)

        self.mask: pygame.Mask = mask
        self.rect: pygame.Rect = self.mask.get_rect()
    

    def set_hitbox(self, mask: pygame.Mask):
        self.mask = mask
        self.rect = self.mask.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y


    def check_collision(self, damage_hitbox: DamageHitbox):
        if self.rect.colliderect(damage_hitbox.rect):
            offset = damage_hitbox.pos-self.pos
            return self.mask.overlap(damage_hitbox.mask, offset=offset)


class Damage(DamageHitbox):
    def __init__(self, game: Game, pos: pygame.Vector2, mask: pygame.Mask = pygame.Mask((0,0))):
        super().__init__(game, pos, mask)

        self.amount: float = 10
