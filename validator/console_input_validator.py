

class InputValidator:
    def __init__(self, allowed_inputs: list = None, min_length: int = 0, max_length: int = 1000):
        self.allowed_inputs = allowed_inputs
        self.min_length = min_length
        self.max_length = max_length

    def validate_by_value(self, input_: str):
        return input_ in self.allowed_inputs

    def validate_by_length(self, input_: str):
        return self.min_length <= len(input_) <= self.max_length
