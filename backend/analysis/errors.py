class InvalidDateRangeError(RuntimeError):
    def __init__(self, message):
            self.message = message
            super().__init__(self.message)


class NoMovementEntryFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoExerciseEntryFoundError(RuntimeError):
    def __init__(self, message):
            self.message = message
            super().__init__(self.message)
            
class NoSetEntriesFoundError(RuntimeError):
    def __init__(self, message):
            self.message = message
            super().__init__(self.message)