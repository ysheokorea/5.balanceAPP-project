from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    # This def _make_hash_value()
    # def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
    #     return super()._make_hash_value(user, timestamp)
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))

account_activation_token = AppTokenGenerator()