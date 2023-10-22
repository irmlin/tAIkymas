import threading
from concurrent.futures.thread import ThreadPoolExecutor

from gamecontroller.game_mode_handlers.base_handler import BaseHandler
from gamecontroller.game_state import GameState
from gamecontroller.utils import generate_animation
from gpt import GPT
from validator import InputValidator

fetching_done = False


class CVModeHandler(BaseHandler):
    def __init__(self, gpt: GPT):
        super().__init__()
        self.__input_validator = InputValidator(min_length=30, max_length=300)
        self.__gpt = gpt
        self.__fetching_done_event = threading.Event()

    def handle(self) -> GameState:

        question = "Generate 3 distinct CVs for fictional individuals in different professions. " \
                   "Then, create a profitable startup idea that these 3 people " \
                   "could do in 3 sentences. Briefly but precisely tell what each" \
                   "person's responsibilities would be and what product they would all sell. " \
                   "Do not use any extensive vocabulary, " \
                   "title the paragraphs 'CVs of 3 people' and 'Startup idea' " \
                   "accordingly."
        response = self.__handle_dialog(question=question, waiting_text='Generating CVs')
        print(response)

        user_startup_idea = self.get_user_input(prompt='Enter your startup idea, which involves these 3 people:')
        question = f"Here is another startup idea for the 3 people: {user_startup_idea}\n\n" \
                   f"Your task is: imagine you are an investor and you are choosing a startup to " \
                   f"invest to. Evaluate your startup idea and the idea I just provided. The business idea " \
                   f"should match skill sets of the 3 people and be profitable, otherwise, it is not " \
                   f"a particularly good idea. Make sure to write concrete arguments as pros and cons, avoid " \
                   f"generic statements. " \
                   f"Do not use any extensive vocabulary, title the paragraph " \
                   f"'Investor's feedback'. I need 3 sentence feedbacks for each idea. " \
                   f"Don't tell me which idea is better just yet and don't summarize at the end."
        response = self.__handle_dialog(question=question, waiting_text='Evaluating your idea')
        print(response)

        additional_arguments = self.get_user_input(prompt='Enter any additional arguments, why your idea is better:')
        question = f"Here are additional arguments, why the second idea is better: {additional_arguments}\n\n" \
                   f"Your task: provide a shor counter argument, why your generated idea is better. Title this " \
                   f"paragraph as 'Counter argument'. " \
                   f"Then, imagine you are the investor again: provide your final statement, which startup you " \
                   f"would invest to. Title the paragraph as 'Investor's final decision' and provide 2 sentences " \
                   f"long reasoning."
        response = self.__handle_dialog(question=question, waiting_text='Making final decision')
        print(response)
        print(f"{'-'*100}")

        return GameState.GREETING

    def __handle_dialog(self, question: str, waiting_text: str) -> str:
        self.__fetching_done_event.clear()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.__handle_request, question)
            # Waiting animation in console
            generate_animation(text=waiting_text, done_event=self.__fetching_done_event)
            result = future.result()

        return result

    def __handle_request(self, question: str) -> str:
        response = self.__gpt.ask(question=question)
        self.__fetching_done_event.set()
        return response

    def get_user_input(self, prompt) -> str:
        while True:
            user_input = input(prompt)

            # Validate input
            if not self.__input_validator.validate_by_length(input_=user_input):
                print(f'Please enter description between {self.__input_validator.min_length}'
                      f' and {self.__input_validator.max_length} characters long!')
                continue

            return user_input
