
from __future__ import annotations

import pygame

from ..state import State, StateMachine

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .fighter import Fighter
    from game import Game


class FighterState(State):
    def __init__(self, fighter):
        super().__init__()
        self.fighter: Fighter = fighter
        self.id: str = self.__class__.__name__.lower()


    def enter(self):
        self.fighter.set_animation(self.id)
        return super().enter()

    
    def switch_to(self, state: str):
        self.fighter.state_machine.set_state(state)
        self.exit()
        return super().switch_to(state)


class FighterStateMachine(StateMachine):
    def __init__(self, fighter: Fighter, initial_state = None):
        super().__init__(initial_state)

        self.fighter = fighter

        self.states = {
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
