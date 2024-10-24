from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = _('Service temporarily unavailable, try again later.')
    default_code = 'service_unavailable'