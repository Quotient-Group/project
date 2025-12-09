
from __future__ import annotations

import pygame

from .entity import Entity
from .damage import DamageHitbox
from .colors import *
from .controller import Controller
from .animation import AnimationManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import StateMachine
    from game import Game


class ControlledEntity(Entity):
    def __init__(self, game: Game, pos: pygame.Vector2, controller: Controller = None):
        super().__init__(game, pos)

        # WHAT CONTROLS THIS ENTITY?
        self.controller: Controller = Controller(self.game)
        if controller:
            self.controller = controller

        # INITIALIZE ANIMATION MANAGER
        self.animation_manager: AnimationManager = AnimationManager(self.game)

        # INITIALIZE STATE MACHINE
        self.state_machine: StateMachine = None

        self.texture: pygame.Surface = None
        self.mask: pygame.Mask = None

        self.damage_hitbox: DamageHitbox = DamageHitbox(self.game, self.pos)
        self.hitbox_color = BLUE

        # STATUS
        self.status: dict = {}

        # INPUTS
        self.inputs = {}

        self.direction_vector: pygame.Vector2 = pygame.Vector2()
        self.flip: pygame.Vector2 = pygame.Vector2()


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

        return super().update(dt)


    def draw(self, hitbox: bool = True):
        # DRAW TEXTURE
        self.game.window.blit(pygame.transform.flip(self.texture, bool(self.flip.x), bool(self.flip.y)), self.pos)

        # IF SET, DRAW THE HITBOX
        if hitbox:
            surf: pygame.Surface = self.damage_hitbox.mask.to_surface(setcolor=(*self.hitbox_color,100), unsetcolor=(0,0,0,0))
            self.game.window.blit(surf, self.pos)

