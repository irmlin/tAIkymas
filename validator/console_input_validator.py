

class InputValidator:
    def __init__(self, allowed_inputs: list):
        self.allowed_inputs = allowed_inputs

    def validate(self, input_: str):
        return input_ in self.allowed_inputs
