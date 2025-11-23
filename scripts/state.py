
from __future__ import annotations

import pygame

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
