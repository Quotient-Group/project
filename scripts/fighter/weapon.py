
from __future__ import annotations

import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from ..entity import Entity


class Weapon(Entity):
    def __init__(self, game: Game, pos: pygame.Vector2):
        super().__init__(game, pos)
