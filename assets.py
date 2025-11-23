
import pygame


# IMPORTANT!!! SPRITESHEETS ARE ASSUMED TO BE LINEAR AND EVERY FRAME IS ASSUMED TO BE A SQUARE


FIGHTER_ASSETS: dict = {
    "masksheets": {
        "idle": pygame.image.load("./assets/fighter/idle_hitbox.png").convert_alpha(),
        "run": pygame.image.load("./assets/fighter/run_hitbox.png").convert_alpha()
    },

    "spritesheets": {
        "idle": pygame.image.load("./assets/fighter/idle.png").convert_alpha(),
        "run": pygame.image.load("./assets/fighter/run.png").convert_alpha(),
    },
}
