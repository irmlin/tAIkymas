from abc import ABC, abstractmethod

from gamecontroller.game_state import GameState


class BaseHandler(ABC):
    def __init__(self):
        self.INVALID_USER_INPUT = '-1'
        super().__init__()

    @abstractmethod
    def handle(self) -> GameState:
        """
        Handle game mode logic and return the following game state.
        """
        pass

    @abstractmethod
    def get_user_input(self) -> str:
        """
        Get input from the user, validate it (preferably) and return it.
        :return:
        """
        pass
