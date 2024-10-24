import requests
from django.core.exceptions import ValidationError as DjangoValidationError
from drf_standardized_errors.handler import ExceptionHandler
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError as DRFValidationError

from api.apps.base.exceptions import ServiceUnavailable


class CustomExceptionHandler(ExceptionHandler):
    def convert_unhandled_exceptions(self, exc: Exception) -> exceptions.APIException:
        if not isinstance(exc, exceptions.APIException):
            if isinstance(exc, DjangoValidationError):
                _code = getattr(exc, "code", None)
                return DRFValidationError(detail=exc.messages, code=_code)
            elif isinstance(exc, requests.Timeout) or isinstance(exc, requests.ConnectionError):
                return ServiceUnavailable()
            else:
                return exceptions.APIException(detail=str(exc))
        else:
            return exc