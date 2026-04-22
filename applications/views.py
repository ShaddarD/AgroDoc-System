from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import InspectionRecord
from .selectors import get_application_queryset
from .services import ApplicationService
from .serializers import (
    ApplicationListSerializer,
    ApplicationReadSerializer,
    ApplicationCreateSerializer,
    ApplicationUpdateSerializer,
    InspectionRecordSerializer,
)

_service = ApplicationService()


class ApplicationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        qs = get_application_queryset()
        return Response(ApplicationListSerializer(qs, many=True).data)

    def retrieve(self, request, pk=None):
        try:
            app = _service.get_by_uuid(pk)
        except Exception:
            raise NotFound()
        return Response(ApplicationReadSerializer(app).data)

    def create(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app = _service.create(serializer.validated_data)
        return Response(ApplicationReadSerializer(app).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        try:
            app = _service.get_by_uuid(pk)
        except Exception:
            raise NotFound()
        serializer = ApplicationUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        app = _service.update(app, serializer.validated_data)
        return Response(ApplicationReadSerializer(app).data)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        try:
            app = _service.get_by_uuid(pk)
        except Exception:
            raise NotFound()
        return Response(_service.preview(app))

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        try:
            app = _service.get_by_uuid(pk)
        except Exception:
            raise NotFound()
        return Response({'documents': _service.get_available_documents(app)})


class InspectionRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionRecordSerializer

    def get_queryset(self):
        return InspectionRecord.objects.select_related('application', 'created_by').all()
