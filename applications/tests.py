import shutil
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from applications.models import (
    Application, ApplicationContainer, ApplicationHistory,
    GeneratedFile, InspectionRecord,
)
from reference.models import ApplicationStatus

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ApplicationsApiTests(APITestCase):

    # setUpTestData: User и статусы — один раз на весь класс (DB не перезаписывается между тестами)
    # setUp:         force_authenticate — нужен на каждый тест (self.client пересоздаётся)

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="operator",
            password="StrongPass123!",
            first_name="Оператор",
            last_name="Системы",
            email="operator@example.com",
        )
        UserProfile.objects.create(
            user=cls.user,
            patronymic="Тестович",
            company_name="ООО Тест",
            inn="7701234567",
        )
        cls.new_status = ApplicationStatus.objects.create(
            code="new", name="Новая", sort_order=1,
        )
        cls.in_progress_status = ApplicationStatus.objects.create(
            code="in_progress", name="В работе", sort_order=2,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    # ── URL-константы ─────────────────────────────────────────────────────
    APP_LIST = "/api/applications/"
    IR_LIST  = "/api/inspection-records/"

    # ── Фабрики ───────────────────────────────────────────────────────────
    def make_application(self, **kwargs) -> Application:
        return Application.objects.create(
            status=self.new_status,
            created_by=self.user,
            **kwargs,
        )

    def make_container(self, application: Application, number="MSKU1234567", **kwargs) -> ApplicationContainer:
        return ApplicationContainer.objects.create(
            application=application,
            container_number=number,
            sort_order=1,
            **kwargs,
        )

    def make_generated_file(self, application: Application, **kwargs) -> GeneratedFile:
        return GeneratedFile.objects.create(
            application=application,
            file_name="test.docx",
            file_path="generated_docs/test.docx",
            file_type="cokz",
            created_by=self.user,
            **kwargs,
        )

    def make_inspection_record(self, **kwargs) -> InspectionRecord:
        return InspectionRecord.objects.create(
            manager="Алексей",
            client="ООО Альфа",
            commodity="Ячмень",
            created_by=self.user,
            **kwargs,
        )

    # ── Application: создание ─────────────────────────────────────────────
    def test_create_sets_created_by_and_generates_number(self):
        r = self.client.post(self.APP_LIST, {}, format="json")

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        app = Application.objects.get(id=r.data["id"])
        self.assertEqual(app.created_by, self.user)
        self.assertTrue(app.application_number.startswith("APP-"))
        self.assertIn("application_number", r.data)

    # ── Application: список ───────────────────────────────────────────────
    def test_list_returns_only_list_serializer_fields(self):
        app = self.make_application(weight_mt="12.500")

        r = self.client.get(self.APP_LIST)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        item = r.data[0]
        self.assertEqual(item["id"], str(app.id))
        for field in ("application_number", "status", "status_name", "status_code", "weight_mt"):
            self.assertIn(field, item)
        # detail-поля не должны просочиться в list-ответ
        self.assertNotIn("containers", item)
        self.assertNotIn("files", item)

    def test_search_filters_by_container_number(self):
        matching = self.make_application()
        other    = self.make_application()
        self.make_container(matching, number="MSKU1234567")
        self.make_container(other,    number="TGHU7654321")

        r = self.client.get(self.APP_LIST, {"search": "MSKU1234567"})

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["id"], str(matching.id))

    # ── Application: поиск по номеру ──────────────────────────────────────
    def test_by_number_returns_detail(self):
        app = self.make_application()

        r = self.client.get(f"/api/applications/by-number/{app.application_number}/")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], str(app.id))
        self.assertEqual(r.data["application_number"], app.application_number)

    # ── Application: смена статуса ────────────────────────────────────────
    def test_change_status_updates_application_and_writes_history(self):
        app = self.make_application()

        r = self.client.post(
            f"/api/applications/{app.id}/change-status/",
            {"status": self.in_progress_status.code},
            format="json",
        )

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        app.refresh_from_db()
        self.assertEqual(app.status, self.in_progress_status)
        self.assertEqual(r.data["status"], self.in_progress_status.code)
        history = ApplicationHistory.objects.filter(application=app).latest("created_at")
        self.assertIn("in_progress", history.action)

    def test_change_status_400_for_unknown_code(self):
        app = self.make_application()

        r = self.client.post(
            f"/api/applications/{app.id}/change-status/",
            {"status": "does_not_exist"},
            format="json",
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        app.refresh_from_db()
        self.assertEqual(app.status, self.new_status)

    # ── Application: генерация документов ────────────────────────────────
    @patch("applications.views.DocumentGenerator")
    def test_generate_documents_creates_files_and_history(self, MockGenerator):
        app = self.make_application()
        MockGenerator.return_value.generate_all.return_value = [
            {"name": "doc1.docx", "path": "generated_docs/2026/04/17/doc1.docx", "type": "cokz"},
            {"name": "doc2.xlsx", "path": "generated_docs/2026/04/17/doc2.xlsx", "type": "act"},
        ]

        r = self.client.post(
            f"/api/applications/{app.id}/generate_documents/", {}, format="json",
        )

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)
        self.assertEqual(GeneratedFile.objects.filter(application=app).count(), 2)
        history = ApplicationHistory.objects.filter(application=app).latest("created_at")
        self.assertEqual(history.action, "Сгенерированы документы")
        self.assertEqual(len(history.changes["files"]), 2)

    # ── Application: файлы ────────────────────────────────────────────────
    def test_files_endpoint_returns_generated_files(self):
        app = self.make_application()
        gf  = self.make_generated_file(app)

        r = self.client.get(f"/api/applications/{app.id}/files/")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["id"], str(gf.id))
        self.assertEqual(r.data[0]["file_name"], "test.docx")

    def test_file_download_404_when_file_missing_on_disk(self):
        app = self.make_application()
        gf  = self.make_generated_file(
            app, file_name="missing.docx", file_path="generated_docs/missing.docx",
        )

        r = self.client.get(f"/api/files/{gf.id}/download/")

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.data["error"], "Файл не найден")

    # ── InspectionRecord ──────────────────────────────────────────────────
    def test_create_inspection_record_sets_created_by(self):
        r = self.client.post(self.IR_LIST, {
            "manager": "Иван",
            "client": "ООО Клиент",
            "commodity": "Пшеница",
            "inspection_date_plan": "2026-04-17",
        }, format="json")

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InspectionRecord.objects.get().created_by, self.user)

    def test_filter_inspection_records_by_manager(self):
        self.make_inspection_record(manager="Алексей", commodity="Ячмень")
        self.make_inspection_record(manager="Мария",   commodity="Кукуруза")

        r = self.client.get(self.IR_LIST, {"manager": "Алекс"})

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["manager"], "Алексей")
