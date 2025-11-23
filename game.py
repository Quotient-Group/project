
from __future__ import annotations

import pygame

import sys
import time

from scripts.colors import *
from scripts.controller import RandomController


WIDTH, HEIGHT = 800, 640

class Game:
    def __init__(self):
        pygame.init()

        self.width, self.height = WIDTH, HEIGHT
        self.size: pygame.Vector2 = pygame.Vector2(self.width, self.height)
        self.display: pygame.Surface = pygame.display.set_mode(self.size)

        from scripts.fighter.fighter import Fighter
        from scripts.damage import DamageHitbox

        self.window: pygame.Surface = pygame.Surface((self.width, self.height))
        self.window_scale = 3
        self.window_offset: pygame.Vector2 = pygame.Vector2()

        self.dt: float = 0
        self.prev_time: float = time.time()

        self.fighter = Fighter(self, pygame.Vector2(50,100))
        self.fighter_2 = Fighter(self, pygame.Vector2(100, 100), controller=RandomController(self))

        self.fighters: list[Fighter] = [self.fighter, self.fighter_2]
        self.damages: list[DamageHitbox] = []


    def update(self):
        self.dt = time.time()-self.prev_time
        self.prev_time = time.time()

        for fighter in self.fighters.copy():
            fighter.update(self.dt)
    

    def draw(self):
        self.window.fill(GRASS)

        for fighter in self.fighters:
            fighter.draw()

        self.display.blit(pygame.transform.scale_by(self.window, self.window_scale), self.window_offset)
        pygame.display.update()


    def run(self):
        while True:
            self.update()
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
