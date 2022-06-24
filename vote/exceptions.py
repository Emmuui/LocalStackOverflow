class TimeValidateException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaseValidateException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RatingException(Exception):
    def __init__(self, message):
        super().__init__(message)
