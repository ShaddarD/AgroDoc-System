from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Account


class AccountsAuthBackend(BaseBackend):
    """Authenticates against the accounts table, syncs Django User for JWT."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            account = Account.objects.get(login=username, is_active=True)
        except Account.DoesNotExist:
            return None

        # Empty password_hash means first-login setup required
        if not account.password_hash:
            return None

        if not check_password(password, account.password_hash):
            return None

        user, _ = User.objects.get_or_create(username=username)
        user.first_name = account.first_name
        user.last_name = account.last_name
        user.email = account.email or ''
        user.is_staff = account.role_code == 'admin'
        user.is_active = True
        user.save(update_fields=['first_name', 'last_name', 'email', 'is_staff', 'is_active'])
        user._account = account
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
