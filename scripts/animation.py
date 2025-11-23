
from __future__ import annotations

import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

class AnimationManager:
    def __init__(self, game: Game):
        self.game: Game = game

        self.damagesheet: pygame.Surface = None
        self.spritesheet: pygame.Surface = None
        self.data: dict = None

        self.animation_time: float = 0
        self.ended = False
    

    def has_ended(self):
        return self.ended and not self.data["loop"]


    def set_animation(self, damagesheet: pygame.Surface, spritesheet: pygame.Surface, data: dict):
        self.damagesheet = damagesheet
        self.spritesheet = spritesheet
        self.data = data

        # IMPORTANT!!! SPRITESHEETS ARE ASSUMED TO BE LINEAR AND EVERY FRAME IS ASSUMED TO BE A SQUARE
        self.length = self.spritesheet.width // self.spritesheet.height

        self.animation_time = 0
        self.ended = False


    def get_frame(self) -> tuple[pygame.Mask, pygame.Surface]:
        # DAMAGE HITBOX
        t: float = self.animation_time / self.data["duration"]
        tex_index: int = (t*self.damagesheet.width) // self.damagesheet.height
        size: int = self.damagesheet.height
        tex: pygame.Surface = self.damagesheet.subsurface(pygame.Rect(tex_index*size, 0, size, size))
        mask: pygame.Mask = pygame.mask.from_surface(tex)

        # TEXTURE
        t: float = self.animation_time / self.data["duration"]
        tex_index: int = (t*self.spritesheet.width) // self.spritesheet.height
        size: int = self.spritesheet.height
        tex: pygame.Surface = self.spritesheet.subsurface(pygame.Rect(tex_index*size, 0, size, size))

        return mask, tex


    def update(self, dt):
        # IF NOT MEANT TO LOOP, THE ANIMATION STOPS WHEN ENDED
        if self.has_ended():
            return

        # OTHERWISE, THE ANIMATION LOOPS
        self.ended = False

        self.animation_time += dt
        if self.animation_time >= self.data["duration"]:
            self.animation_time = 0
            self.ended = True
