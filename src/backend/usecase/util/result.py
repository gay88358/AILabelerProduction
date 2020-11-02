class Result:
    def __init__(self):
        pass

    @staticmethod
    def success(value):
        return Success(value)

    @staticmethod
    def failure(error_messages):
        return Failure(error_messages)

    def flat_map(self, func):
        pass

    def is_success(self):
        raise ValueError('is_success need to implemented')

class Success:
    def __init__(self, value):
        self.value = value

    def flat_map(self, func):
        return func(self.value)
    
    def is_success(self):
        return True

class Failure:
    def __init__(self, error_messages):
        if type(error_messages) is not list:
            raise ValueError("Failure object only accept list of string")

        self.error_messages = error_messages

    def flat_map(self, func):
        return self
    
    def is_success(self):
        return False
