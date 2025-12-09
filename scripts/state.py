
from __future__ import annotations

import pygame

from .controlled_entity import ControlledEntity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class State:
    def __init__(self):
        ...
    

    def switch_to(self, state):
        ...


    def enter(self):
        ...
    

    def update(self, dt):
        ...
    

    def exit(self):
        ...


class StateMachine:
    def __init__(self, initial_state: State | None = None):
        self.states: dict[State] = {}
        self.current_state: State | None = initial_state


    def set_state(self, state: str):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[state]
        self.current_state.enter()


    def update(self, dt):
        self.current_state.update(dt)


class ControlledEntityState(State):
    def __init__(self, entity):
        super().__init__()
        self.entity: ControlledEntity = entity
        self.id: str = self.__class__.__name__.lower()


    def enter(self):
        self.fighter.set_animation(self.id)
        return super().enter()

    
    def switch_to(self, state: str):
        self.fighter.state_machine.set_state(state)
        self.exit()
        return super().switch_to(state)
