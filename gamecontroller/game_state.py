from enum import Enum


class GameState(Enum):
    GREETING = 1
    CHOOSE_GAME_MODE = 2
    GAME_MODE_CV = 3
    GAME_MODE_ORGANISATION = 4
    GAME_MODE_QUIZ = 5
    EXIT = 6

