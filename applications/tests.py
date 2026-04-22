from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from applications.models import Application, InspectionRecord


class ApplicationSmokeTest(APITestCase):
    """
    Smoke tests for the Application API.
    These tests verify basic endpoint availability and authentication requirements.
    Full integration tests require factory-boy fixtures and are tracked separately.
    """

    APP_LIST = '/api/applications/'
    IR_LIST = '/api/applications/inspection-records/'

    def test_list_requires_auth(self):
        r = self.client.get(self.APP_LIST)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inspection_records_requires_auth(self):
        r = self.client.get(self.IR_LIST)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_requires_auth(self):
        r = self.client.post(self.APP_LIST, {}, format='json')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class DummyUser:
    """Explicit stub — no MagicMock magic that could mask attribute errors."""
    is_authenticated = True
    is_active = True
    pk = 'test-user-stub'


class ApplicationImportSmokeTest(SimpleTestCase):

    def test_core_modules_importable(self):
        import applications.urls    # noqa: F401
        import applications.views   # noqa: F401
        import applications.admin   # noqa: F401

    def test_services_and_selectors_importable(self):
        from applications.services import ApplicationService, MasterApplicationService   # noqa: F401
        from applications.selectors import get_application_queryset, ApplicationDocumentResolver  # noqa: F401

    def test_serializers_importable(self):
        from applications.serializers import (  # noqa: F401
            ApplicationListSerializer, ApplicationReadSerializer,
            ApplicationCreateSerializer, ApplicationUpdateSerializer,
            InspectionRecordSerializer,
        )


class ApplicationSerializerContractTest(SimpleTestCase):

    def test_list_serializer_exposes_status_code_not_status(self):
        from applications.serializers import ApplicationListSerializer
        fields = ApplicationListSerializer().fields
        self.assertIn('status_code', fields)
        self.assertNotIn('status', fields)

    def test_read_serializer_exposes_status_code_not_status(self):
        from applications.serializers import ApplicationReadSerializer
        fields = ApplicationReadSerializer().fields
        self.assertIn('status_code', fields)
        self.assertNotIn('status', fields)

    def test_read_serializer_status_code_source(self):
        # ModelSerializer FK fields break on stub objects (serializable_value protocol)
        # — verify field wiring via source attribute instead
        from applications.serializers import ApplicationReadSerializer
        fields = ApplicationReadSerializer().fields
        self.assertEqual(fields['status_code'].source, 'status_id')

    def test_read_serializer_status_description_source(self):
        from applications.serializers import ApplicationReadSerializer
        fields = ApplicationReadSerializer().fields
        self.assertEqual(fields['status_description'].source, 'status.description')


class ApplicationEndpointSmokeTest(APITestCase):
    """Fully isolated via mocks — no DB required."""

    def setUp(self):
        self.client.force_authenticate(user=DummyUser())

    def test_list_returns_200_empty(self):
        with patch('applications.views.get_application_queryset', return_value=[]):
            r = self.client.get('/api/applications/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, [])

    def _patch_not_found(self):
        return patch(
            'applications.views._service.get_by_uuid',
            side_effect=Application.DoesNotExist,
        )

    def test_retrieve_not_found_returns_404(self):
        import uuid
        with self._patch_not_found():
            r = self.client.get(f'/api/applications/{uuid.uuid4()}/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_preview_not_found_returns_404(self):
        import uuid
        with self._patch_not_found():
            r = self.client.get(f'/api/applications/{uuid.uuid4()}/preview/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_documents_not_found_returns_404(self):
        import uuid
        with self._patch_not_found():
            r = self.client.get(f'/api/applications/{uuid.uuid4()}/documents/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_ikr_number_without_ikr_date_returns_400(self):
        r = self.client.post('/api/applications/', {
            'ikr_number': 'ИКР-2026-001',
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ikr_date', r.data)
