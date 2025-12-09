
from __future__ import annotations

import pygame

from ..controlled_entity import ControlledEntity
from ..damage import DamageHitbox
from ..colors import *
from ..controller import Controller, PlayerController, RandomController
from ..animation import AnimationManager
from .fighter_states import FighterStateMachine
from assets import FIGHTER_ASSETS

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Fighter(ControlledEntity):

    assets = FIGHTER_ASSETS

    animations_data = {
        "idle": {
            "duration": 2,
            "loop": True
        },
        "run": {
            "duration": 0.7,
            "loop": True
        },
    }

    def __init__(self, game: Game, pos: pygame.Vector2, controller: Controller = None):
        super().__init__(game, pos)

        # WHAT CONTROLS THIS FIGHTER?
        self.controller: PlayerController = PlayerController(self.game)
        if controller:
            self.controller = controller

        # INITIALIZE ANIMATION MANAGER
        self.animation_manager: AnimationManager = AnimationManager(self.game)

        # INITIALIZE STATE MACHINE
        self.state_machine: FighterStateMachine = FighterStateMachine(self)

        self.texture: pygame.Surface = None
        self.mask: pygame.Mask = None

        self.damage_hitbox: DamageHitbox = DamageHitbox(self.game, self.pos)
        self.hitbox_color = BLUE

        # STATUS
        self.status: dict = {
            "alive": True,
            "max_health": 100,
            "health": 100,
            "speed": 100
        }

        # INPUTS
        self.inputs = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            "attack": False,
        }

        # INITIALIZE AT IDLE
        self.set_animation("idle")


    def get_hurt(self, damage_amount: float):
        # REDUCE HEALTH
        self.status["health"] = max(0, self.status["health"]-damage_amount)

        # CHECK IF DEAD
        if self.status["health"] == 0:
            self.status["alive"] = False


    def handle_damage(self, damage: DamageHitbox):
        # CHECK FOR COLLISION
        if self.damage_hitbox.check_collision(damage):
            self.get_hurt(damage.amount)


    def update(self, dt: float):
        if any([(self!=fighter and self.damage_hitbox.check_collision(fighter.damage_hitbox)) for fighter in self.game.fighters]):
            self.hitbox_color = RED
        else:
            self.hitbox_color = BLUE

        return super().update(dt)

