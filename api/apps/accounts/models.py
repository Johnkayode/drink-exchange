import uuid
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from api.apps.accounts.managers import UserManager
from api.apps.base.models import BaseModel


class AccountType(models.TextChoices):
    COMPANY_ADMIN = "company_admin", _("Company Admin")
    COMPANY_STAFF = "company_staff", _("Company Staff")
    CUSTOMER = "customer", _("Customer")
  

class Business(BaseModel):
    name = models.CharField(_("business name"),
        max_length=100,
        blank=False,
        null=True,
    )
    email = models.CharField(_("email address"), max_length=50, unique=True, blank=True, null=True)
    is_account_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.business_name


class User(AbstractUser):
    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)

    phone_number = PhoneNumberField(_("phone number"), unique=True, blank=True)
    phone_number_verified = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    deleted_at = models.DateTimeField(_("deleted"), null=True, blank=True)

    account_type = models.CharField(choices=AccountType.choices, null=True, blank=True)
    business = models.ForeignKey(Business, related_name="members", on_delete=models.SET_NULL, null=True, blank=True)
    
    objects = UserManager() 


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def full_name(self) -> str:
        return self.get_full_name()
    
    def __repr__(self):
        return "<%s: %s>" % (self.full_name, self.email or self.phone_number)
    
    @property
    def email_verified(self) -> bool:
        return EmailAddress.objects.filter(email=self.email, verified=True).exists()
    
    def send_email( 
        self,
        subject: str,
        template_name: str,
        context: dict,
        from_email: str = settings.DEFAULT_FROM_EMAIL,
        **kwargs,
    ):
        ...
    
    
