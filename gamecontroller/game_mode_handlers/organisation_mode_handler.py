from gamecontroller.game_messages import INVALID_OPTION_MESSAGE, CHOOSE_GAME_MODE_MENU_MESSAGE
from gamecontroller.game_mode_handlers.base_handler import BaseHandler
from gamecontroller.game_state import GameState
from gpt import GPT
from validator import InputValidator


class OrganisationModeHandler(BaseHandler):
    def __init__(self, gpt: GPT):
        super().__init__()
        self.__input_message = CHOOSE_GAME_MODE_MENU_MESSAGE
        self.__input_validator = InputValidator(min_length=30, max_length=300)
        self.__gpt = gpt

    def handle(self) -> GameState:
        print('This game mode is not implemented yet!')
        return GameState.CHOOSE_GAME_MODE

    def get_user_input(self, prompt: str):
        user_input = input(prompt)

        # Validate input
        if not self.__input_validator.validate_by_length(input_=user_input):
            print(INVALID_OPTION_MESSAGE)
            return self.INVALID_USER_INPUT

        return user_input
