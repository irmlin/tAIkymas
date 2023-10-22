from gamecontroller.game_messages import EXIT_MESSAGE
from gamecontroller.game_mode_handlers import GreetingModeHandler
from gamecontroller.game_mode_handlers.choose_game_mode_handler import ChooseGameModeHandler
from gamecontroller.game_mode_handlers.cv_mode_handler import CVModeHandler
from gamecontroller.game_mode_handlers.organisation_mode_handler import OrganisationModeHandler
from gamecontroller.game_state import GameState
from gpt import GPT


class GameStateHandlerNotImplementedError(BaseException):
    pass


class Controller:
    def __init__(self):
        self.__game_state = GameState.GREETING
        self.__gpt = GPT()
        # Call once
        self.__gpt.new_chat()
        self.__handlers = {
            GameState.GREETING: GreetingModeHandler(),
            GameState.CHOOSE_GAME_MODE: ChooseGameModeHandler(),
            GameState.GAME_MODE_CV: CVModeHandler(gpt=self.__gpt),
            GameState.GAME_MODE_ORGANISATION: OrganisationModeHandler(gpt=self.__gpt)
        }

    def main_loop(self):
        while self.__game_state != GameState.EXIT:
            if self.__game_state not in self.__handlers:
                raise GameStateHandlerNotImplementedError(f'Game state {self.__game_state} has no handler assigned!')
            handler = self.__handlers[self.__game_state]
            self.__game_state = handler.handle()

        print(EXIT_MESSAGE)
