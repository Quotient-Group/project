
from __future__ import annotations

import pygame

from ..entity import Entity
from ..damage import DamageHitbox
from ..colors import *
from ..controller import Controller, PlayerController, RandomController
from ..animation import AnimationManager
from .fighter_states import FighterStateMachine
from assets import FIGHTER_ASSETS

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Fighter(Entity):

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

        # INITIALIZE ANIMATION STUFF
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

        self.direction_vector: pygame.Vector2 = pygame.Vector2()
        self.flip: pygame.Vector2 = pygame.Vector2()

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


    def set_animation(self, anim_id: str):
        # RETRIEVE THE ANIMATION ASSETS AND DATA
        masksheet: pygame.Surface = self.assets["masksheets"][anim_id]
        spritesheet: pygame.Surface = self.assets["spritesheets"][anim_id]
        data: dict = self.animations_data[anim_id]

        # SET THE ANIMATION
        self.animation_manager.set_animation(masksheet, spritesheet, data)


    def update(self, dt: float):
        # UPDATE STUFF
        self.controller.update(self, dt)
        self.state_machine.update(dt)
        self.animation_manager.update(dt)

        # GET CURRENT FRAME
        self.mask, self.texture = self.animation_manager.get_frame()

        # UPDATE DAMAGE HITBOX
        self.damage_hitbox.set_hitbox(self.mask)

        if any([(self!=fighter and self.damage_hitbox.check_collision(fighter.damage_hitbox)) for fighter in self.game.fighters]):
            self.hitbox_color = RED
        else:
            self.hitbox_color = BLUE

        return super().update(dt)


    def draw(self, hitbox: bool = True):
        # DRAW TEXTURE
        self.game.window.blit(pygame.transform.flip(self.texture, bool(self.flip.x), bool(self.flip.y)), self.pos)

        # IF SET, DRAW THE HITBOX
        if hitbox:
            surf: pygame.Surface = self.damage_hitbox.mask.to_surface(setcolor=(*self.hitbox_color,100), unsetcolor=(0,0,0,0))
            self.game.window.blit(surf, self.pos)

