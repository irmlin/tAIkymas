from gamecontroller.game_messages import EXIT_MESSAGE
from gamecontroller.game_mode_handlers import GreetingModeHandler
from gamecontroller.game_mode_handlers.choose_game_mode_handler import ChooseGameModeHandler
from gamecontroller.game_mode_handlers.cv_mode_handler import CVModeHandler
from gamecontroller.game_mode_handlers.organisation_mode_handler import OrganisationModeHandler
from gamecontroller.game_state import GameState


class Controller:
    def __init__(self):
        self.__game_state = GameState.GREETING
        self.__greeting_handler = GreetingModeHandler()
        self.__choose_game_mode_handler = ChooseGameModeHandler()
        self.__cv_mode_handler = CVModeHandler()
        self.__organisation_mode_handler = OrganisationModeHandler()

    def __handle_greeting(self):
        new_game_state = self.__greeting_handler.handle()
        self.__game_state = new_game_state

    def __handle_choose_game_mode(self):
        new_game_state = self.__choose_game_mode_handler.handle()
        self.__game_state = new_game_state

    def __handle_game_mode_CV(self):
        new_game_state = self.__cv_mode_handler.handle()
        self.__game_state = new_game_state

    def __handle_game_mode_organisation(self):
        new_game_state = self.__organisation_mode_handler.handle()
        self.__game_state = new_game_state

    def __handle_exit(self):
        print(EXIT_MESSAGE)
        exit(0)

    def main_loop(self):
        while True:
            if self.__game_state == GameState.GREETING:
                self.__handle_greeting()
            elif self.__game_state == GameState.CHOOSE_GAME_MODE:
                self.__handle_choose_game_mode()
            elif self.__game_state == GameState.GAME_MODE_CV:
                self.__handle_game_mode_CV()
            elif self.__game_state == GameState.GAME_MODE_ORGANISATION:
                self.__handle_game_mode_organisation()
            elif self.__game_state == GameState.EXIT:
                self.__handle_exit()

