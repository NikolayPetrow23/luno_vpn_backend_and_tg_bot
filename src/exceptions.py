from typing import Optional
from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    @classmethod
    def set_detail(cls, detail: str):
        return cls(detail)

    def __init__(self, detail: Optional[str] = None):
        if detail is not None:
            self.detail = detail

        super().__init__(status_code=self.status_code, detail=self.detail)


class ExceptionInCreatingPayment(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""


class ShortLinkNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ""


class SubscriptionActiveException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""


class PlanNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ""


class PaymentTypeNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ""


class PaymentIsAlreadyConfirmed(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""


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


class IncorrectTgDataException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""


class UserIsNotPresentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserSearchExcpetion(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""


class UserCraeateException(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""


