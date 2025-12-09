
from __future__ import annotations

import pygame

from ..controlled_entity import ControlledEntity
from ..damage import Damage

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...


class Weapon(ControlledEntity):
    def __init__(self, game, pos, controller = None):
        super().__init__(game, pos, controller)
        
        self.damage_hitbox: Damage = Damage(self.game, self.pos)

