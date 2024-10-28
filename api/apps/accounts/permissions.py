from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from api.apps.accounts.models import AccountType


class BusinessAdminPermission(BasePermission):
    """
    Allows access only to business accounts.
    """
    
    message = _("You don't have necessary permissions.")
    code = "is_not_business_admin"

    def has_permission(self, request, view):
        return request.user.account_type == AccountType.BUSINESS_ADMIN
    

class BusinessStaffPermission(BasePermission):
    """
    Allows access only to business staff accounts.
    """
    
    message = _("You don't have necessary permissions.")
    code = "is_not_business_staff"

    def has_permission(self, request, view):
       return request.user.account_type == AccountType.BUSINESS_STAFF