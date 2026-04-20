from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile


class AccountsApiTests(APITestCase):
    def setUp(self):
        self.user_password = "StrongPass123!"
        self.user = User.objects.create_user(
            username="employee",
            password=self.user_password,
            first_name="Иван",
            last_name="Иванов",
            email="employee@example.com",
        )
        UserProfile.objects.create(
            user=self.user,
            patronymic="Иванович",
            company_name="ООО Ромашка",
            inn="7701234567",
        )

        self.admin_password = "AdminPass123!"
        self.admin = User.objects.create_superuser(
            username="admin",
            password=self.admin_password,
            email="admin@example.com",
        )

        self.login_url = "/api/accounts/login/"
        self.logout_url = "/api/accounts/logout/"
        self.me_url = "/api/accounts/me/"
        self.register_url = "/api/accounts/register/"
        self.inn_lookup_url = "/api/accounts/inn-lookup/"

    def test_login_returns_tokens_and_user_payload(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": self.user_password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["username"], self.user.username)
        self.assertEqual(response.data["user"]["company_name"], "ООО Ромашка")
        self.assertEqual(response.data["user"]["inn"], "7701234567")

    def test_login_with_invalid_credentials_returns_401(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": "wrong-password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])

    def test_me_requires_authentication(self):
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_current_user_profile_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["first_name"], "Иван")
        self.assertEqual(response.data["last_name"], "Иванов")
        self.assertEqual(response.data["patronymic"], "Иванович")
        self.assertEqual(response.data["company_name"], "ООО Ромашка")
        self.assertEqual(response.data["inn"], "7701234567")

    def test_register_requires_admin(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "username": "new_user",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Петр",
            "last_name": "Петров",
            "email": "new_user@example.com",
            "patronymic": "Петрович",
            "company_name": "ООО Новая Компания",
            "inn": "7707654321",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_register_user_and_profile_is_created(self):
        self.client.force_authenticate(user=self.admin)

        payload = {
            "username": "new_user",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Петр",
            "last_name": "Петров",
            "email": "new_user@example.com",
            "patronymic": "Петрович",
            "company_name": "ООО Новая Компания",
            "inn": "7707654321",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["user"]["username"], "new_user")
        self.assertTrue(User.objects.filter(username="new_user").exists())

        created_user = User.objects.get(username="new_user")
        self.assertTrue(hasattr(created_user, "profile"))
        self.assertEqual(created_user.profile.company_name, "ООО Новая Компания")
        self.assertEqual(created_user.profile.inn, "7707654321")

    def test_register_rejects_password_mismatch(self):
        self.client.force_authenticate(user=self.admin)

        payload = {
            "username": "bad_user",
            "password": "StrongPass123!",
            "password2": "AnotherPass123!",
            "first_name": "Петр",
            "last_name": "Петров",
            "email": "bad_user@example.com",
            "patronymic": "Петрович",
            "company_name": "ООО Ошибка",
            "inn": "7707654321",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", str(response.data).lower())

    @override_settings(DADATA_TOKEN="")
    def test_inn_lookup_without_token_returns_503(self):
        response = self.client.get(self.inn_lookup_url, {"inn": "7707083893"})

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn("DADATA_TOKEN", response.data["error"])

    def test_logout_returns_success_for_authenticated_user(self):
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": self.user_password,
            },
            format="json",
        )
        refresh = login_response.data["refresh"]

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.logout_url,
            {"refresh": refresh},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])