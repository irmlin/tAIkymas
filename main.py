from gamecontroller import Controller
from gamecontroller.game_mode_handlers import GreetingModeHandler

if __name__ == '__main__':
    game_controller = Controller()

    # Start the game
    game_controller.main_loop()
