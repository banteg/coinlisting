class BaseExchangeException(BaseException):
    pass


class InvalidResponseException(BaseExchangeException):
    pass


class WrongContentTypeException(BaseExchangeException):
    pass
