from gamecontroller.game_messages import INVALID_OPTION_MESSAGE, CHOOSE_GAME_MODE_MENU_MESSAGE
from gamecontroller.game_mode_handlers.base_handler import BaseHandler
from gamecontroller.game_state import GameState
from validator import InputValidator


class ChooseGameModeHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.__input_message = CHOOSE_GAME_MODE_MENU_MESSAGE
        self.__allowed_inputs = ['1', '2', '3', '4', '5']
        self.__input_validator = InputValidator(allowed_inputs=self.__allowed_inputs)

    def handle(self) -> GameState:
        user_input = self.get_user_input(self.__input_message)

        if user_input == '1':
            next_game_state = GameState.GAME_MODE_CV
        elif user_input == '2':
            next_game_state = GameState.GAME_MODE_ORGANISATION
        elif user_input == '3':
            next_game_state = GameState.GAME_MODE_QUIZ
        elif user_input == '4':
            next_game_state = GameState.GREETING
        elif user_input == self.INVALID_USER_INPUT:
            next_game_state = GameState.CHOOSE_GAME_MODE
        else:
            next_game_state = GameState.EXIT

        return next_game_state

    def get_user_input(self, prompt: str):
        user_input = input(prompt)

        # Validate input
        if not self.__input_validator.validate_by_value(input_=user_input):
            print(INVALID_OPTION_MESSAGE)
            return self.INVALID_USER_INPUT

        return user_input
