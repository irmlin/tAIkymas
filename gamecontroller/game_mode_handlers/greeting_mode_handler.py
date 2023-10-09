from gamecontroller.game_messages import GREETING_MESSAGE, INVALID_OPTION_MESSAGE, GAME_PURPOSE_MESSAGE, \
    PLAYER_GOAL_MESSAGE, GAME_RULES_MESSAGE
from gamecontroller.game_mode_handlers.base_handler import BaseHandler
from gamecontroller.game_state import GameState
from validator import InputValidator


class GreetingModeHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.__input_message = GREETING_MESSAGE
        self.__allowed_inputs = ['1', '2', '3', '4', '5']
        self.__input_validator = InputValidator(allowed_inputs=self.__allowed_inputs)

    def handle(self) -> GameState:
        user_input = self.get_user_input()

        if user_input == '1':
            print(GAME_PURPOSE_MESSAGE)
            next_game_state = GameState.GREETING
        elif user_input == '2':
            print(PLAYER_GOAL_MESSAGE)
            next_game_state = GameState.GREETING
        elif user_input == '3':
            print(GAME_RULES_MESSAGE)
            next_game_state = GameState.GREETING
        elif user_input == '4':
            next_game_state = GameState.CHOOSE_GAME_MODE
        elif user_input == self.INVALID_USER_INPUT:
            next_game_state = GameState.GREETING
        else:
            next_game_state = GameState.EXIT

        return next_game_state

    def get_user_input(self) -> str:
        user_input = input(self.__input_message)

        # Validate input
        if not self.__input_validator.validate(input_=user_input):
            print(INVALID_OPTION_MESSAGE)
            return self.INVALID_USER_INPUT

        return user_input
