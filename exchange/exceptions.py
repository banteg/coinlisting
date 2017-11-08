class BaseExchangeException(Exception):
    pass


class InvalidResponseException(BaseExchangeException):
    pass


class WrongContentTypeException(BaseExchangeException):
    pass
