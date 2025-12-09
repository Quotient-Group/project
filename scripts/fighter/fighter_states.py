
from __future__ import annotations

import pygame

from ..state import ControlledEntityState, StateMachine

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .fighter import Fighter
    from game import Game


class FighterState(ControlledEntityState):
    def __init__(self, entity):
        super().__init__(entity)
        self.fighter = self.entity


class FighterStateMachine(StateMachine):
    def __init__(self, fighter: Fighter, initial_state = None):
        super().__init__(initial_state)

        self.fighter: Fighter = fighter

        self.states: dict[FighterState] = {
            "idle": Idle(self.fighter),
            "run": Run(self.fighter),
            "attack": Attack(self.fighter),
        }

        self.set_state("idle")
    

    def set_state(self, state):
        return super().set_state(state)


class Idle(FighterState):
    def update(self, dt):
        # GET THE DIRECTION WHERE FIGHTER IS MOVING
        self.fighter.direction_vector = pygame.Vector2(self.fighter.inputs["right"]-self.fighter.inputs["left"], self.fighter.inputs["down"]-self.fighter.inputs["up"])

        # IF FIGHTER MOVES, SWITCH TO RUN
        if self.fighter.direction_vector:
            self.switch_to("run")
            return

        if self.fighter.inputs["attack"]:
            self.switch_to("attack")
            return

        return super().update(dt)


class Run(FighterState):
    def update(self, dt):
        # GET THE DIRECTION WHERE FIGHTER IS MOVING
        self.fighter.direction_vector = pygame.Vector2(self.fighter.inputs["right"]-self.fighter.inputs["left"], self.fighter.inputs["down"]-self.fighter.inputs["up"])
        
        # HANDLE TEXTURE FLIPPING
        if self.fighter.direction_vector.x > 0:
            self.fighter.flip.x = 0
        if self.fighter.direction_vector.x < 0:
            self.fighter.flip.x = 1

        # IF FIGHTER IS NOT MOVING, RETURN TO IDLE
        if not self.fighter.direction_vector:
            self.switch_to("idle")
            return

        if self.fighter.inputs["attack"]:
            self.switch_to("attack")
            return
        
        # IF EVERYTHING IS OK, THEN THE VELOCITY IS JUST THE FIGHTER'S SPEED TIMES THE NORMALIZED DIRECTION VECTOR
        self.fighter.vel = self.fighter.status["speed"]*self.fighter.direction_vector.normalize()

        return super().update(dt)

    def exit(self):
        # RESET FIGHTER VELOCITY (OTHERWISE IT NEVER STOPS)
        self.fighter.vel = pygame.Vector2(0,0)

        return super().exit()


class Attack(FighterState):
    def update(self, dt):
        if self.fighter.animation_manager.has_ended():
            self.switch_to("idle")
