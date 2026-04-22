from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsImportSmokeTest(SimpleTestCase):
    """Verify accounts modules (including models.py being changed) import without errors."""

    def test_accounts_modules_importable(self):
        import accounts.models       # noqa: F401
        import accounts.urls         # noqa: F401
        import accounts.views        # noqa: F401
        import accounts.serializers  # noqa: F401


class AccountsAuthSmokeTest(APITestCase):
    """
    Auth endpoint availability checks.
    Full integration tests (with real Account DB records) tracked separately.
    """

    ME_URL = '/api/accounts/me/'

    def test_me_requires_authentication(self):
        r = self.client.get(self.ME_URL)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
