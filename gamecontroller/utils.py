import sys
import threading
import time
from colorama import init, Fore

init(autoreset=True)


def generate_animation(text: str, done_event: threading.Event):
    sys.stdout.write(f'{Fore.RED}\n{text}')
    while not done_event.is_set():  # Check if the event is signaled
        for i in range(4):
            if done_event.is_set():
                break
            anim_text = '' if i == 0 else '.'
            sys.stdout.write(f'{Fore.RED}{anim_text}')
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write(f'{Fore.RED}\r{text}   \r{text}')
        sys.stdout.flush()
    sys.stdout.write(f'\n\n')
    sys.stdout.flush()
