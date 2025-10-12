from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь c таким номером телефона или почтой уже существует"


class IncorrectEmailOrPasswordException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Неверная почта или пароль"


class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек."


class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует."


class OtpCodeExistsException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный код!"


class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена."


class UserIsNotPresentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
