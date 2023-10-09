from gamecontroller.game_messages import INVALID_OPTION_MESSAGE, CHOOSE_GAME_MODE_MENU_MESSAGE
from gamecontroller.game_mode_handlers.base_handler import BaseHandler
from gamecontroller.game_state import GameState
from validator import InputValidator


class CVModeHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.__input_message = CHOOSE_GAME_MODE_MENU_MESSAGE
        self.__allowed_inputs = ['1', '2', '3', '4']
        self.__input_validator = InputValidator(allowed_inputs=self.__allowed_inputs)

    def handle(self) -> GameState:
        print('This game mode is not implemented yet!')
        return GameState.CHOOSE_GAME_MODE

    def get_user_input(self):
        user_input = input(self.__input_message)

        # Validate input
        if not self.__input_validator.validate(input_=user_input):
            print(INVALID_OPTION_MESSAGE)
            return self.INVALID_USER_INPUT

        return user_input
