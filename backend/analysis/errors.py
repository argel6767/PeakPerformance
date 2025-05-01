class InvalidDateRangeError(RuntimeError):
    def __init__(self, message):
            self.message = message
            super().__init__(self.message)


class NoExerciseEntryFound(RuntimeError):
    def __init__(self, message):
            self.message = message
            super().__init__(self.message)
            
class NoSetEntriesFound(RuntimeError):
    def __init__(self, message):
            self.message = message
            super().__init__(self.message)