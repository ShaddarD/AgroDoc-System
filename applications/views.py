from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
from django.http import FileResponse
from django.db import models
import os

from .models import (
    Application, ApplicationContainer, ApplicationCertificate,
    ApplicationRegulation, GeneratedFile, ApplicationHistory, InspectionRecord,
)
from .serializers import (
    ApplicationListSerializer, ApplicationDetailSerializer, ApplicationCreateSerializer,
    ApplicationContainerSerializer, ApplicationCertificateSerializer,
    ApplicationRegulationSerializer, GeneratedFileSerializer,
    InspectionRecordSerializer, ApplicationHistorySerializer,
)
from reference.models import ApplicationStatus


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Application.objects.select_related(
            'status', 'sender_ru', 'receiver', 'product',
            'import_country', 'created_by',
        )

        status_code = self.request.query_params.get('status')
        if status_code:
            qs = qs.filter(status__code=status_code)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                models.Q(application_number__icontains=search) |
                models.Q(product__name_ru__icontains=search) |
                models.Q(receiver__name_en__icontains=search) |
                models.Q(containers__container_number__icontains=search)
            ).distinct()

        date_from = self.request.query_params.get('date_from')
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ApplicationCreateSerializer
        return ApplicationDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # --- Containers ---

    @action(detail=True, methods=['get', 'post'], url_path='containers')
    def containers(self, request, pk=None):
        application = self.get_object()
        if request.method == 'GET':
            serializer = ApplicationContainerSerializer(
                application.containers.all(), many=True
            )
            return Response(serializer.data)
        serializer = ApplicationContainerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(application=application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=['patch', 'delete'],
        url_path=r'containers/(?P<container_pk>[^/.]+)'
    )
    def container_detail(self, request, pk=None, container_pk=None):
        application = self.get_object()
        container = get_object_or_404(ApplicationContainer, pk=container_pk, application=application)
        if request.method == 'DELETE':
            container.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ApplicationContainerSerializer(container, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # --- Certificates ---

    @action(detail=True, methods=['get', 'post'], url_path='certificates')
    def certificates(self, request, pk=None):
        application = self.get_object()
        if request.method == 'GET':
            serializer = ApplicationCertificateSerializer(
                application.certificates.select_related('certificate'), many=True
            )
            return Response(serializer.data)
        serializer = ApplicationCertificateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(application=application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=['patch', 'delete'],
        url_path=r'certificates/(?P<cert_pk>[^/.]+)'
    )
    def certificate_detail(self, request, pk=None, cert_pk=None):
        application = self.get_object()
        cert = get_object_or_404(ApplicationCertificate, pk=cert_pk, application=application)
        if request.method == 'DELETE':
            cert.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ApplicationCertificateSerializer(cert, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # --- Regulations ---

    @action(detail=True, methods=['get', 'post'], url_path='regulations')
    def regulations(self, request, pk=None):
        application = self.get_object()
        if request.method == 'GET':
            serializer = ApplicationRegulationSerializer(
                application.regulations.select_related('regulation'), many=True
            )
            return Response(serializer.data)
        serializer = ApplicationRegulationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(application=application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=['patch', 'delete'],
        url_path=r'regulations/(?P<reg_pk>[^/.]+)'
    )
    def regulation_detail(self, request, pk=None, reg_pk=None):
        application = self.get_object()
        reg = get_object_or_404(ApplicationRegulation, pk=reg_pk, application=application)
        if request.method == 'DELETE':
            reg.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ApplicationRegulationSerializer(reg, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # --- Status change ---

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        application = self.get_object()
        code = request.data.get('status')
        try:
            new_status = ApplicationStatus.objects.get(code=code)
        except ApplicationStatus.DoesNotExist:
            return Response({'error': 'Неверный код статуса'}, status=status.HTTP_400_BAD_REQUEST)

        old_code = application.status.code if application.status else None
        application.status = new_status
        application.save()

        ApplicationHistory.objects.create(
            application=application,
            user=request.user,
            action=f'Изменен статус: {old_code} -> {code}',
        )
        return Response({'status': code})

    # --- Files ---

    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        application = self.get_object()
        serializer = GeneratedFileSerializer(application.files.all(), many=True)
        return Response(serializer.data)

    # --- History ---

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationHistorySerializer(application.history.all(), many=True)
        return Response(serializer.data)

    # --- By number ---

    @action(detail=False, methods=['get'], url_path=r'by-number/(?P<number>[^/.]+)')
    def by_number(self, request, number=None):
        application = get_object_or_404(Application, application_number=number)
        serializer = ApplicationDetailSerializer(application)
        return Response(serializer.data)

    # --- Document generation ---

    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        application = self.get_object()
        try:
            from .document_generator import DocumentGenerator
            generator = DocumentGenerator()
            files = generator.generate_all(application)

            generated_files = []
            for file_info in files:
                file_obj = GeneratedFile.objects.create(
                    application=application,
                    file_name=file_info['name'],
                    file_path=file_info['path'],
                    file_type=file_info['type'],
                    created_by=request.user,
                )
                generated_files.append(file_obj)

            ApplicationHistory.objects.create(
                application=application,
                user=request.user,
                action='Сгенерированы документы',
                changes={'files': [f.file_name for f in generated_files]},
            )

            serializer = GeneratedFileSerializer(generated_files, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InspectionRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = InspectionRecordSerializer

    def get_queryset(self):
        qs = InspectionRecord.objects.all()
        manager = self.request.query_params.get('manager')
        if manager:
            qs = qs.filter(manager__icontains=manager)
        client = self.request.query_params.get('client')
        if client:
            qs = qs.filter(client__icontains=client)
        commodity = self.request.query_params.get('commodity')
        if commodity:
            qs = qs.filter(commodity__icontains=commodity)
        date_from = self.request.query_params.get('date_from')
        if date_from:
            qs = qs.filter(inspection_date_plan__gte=date_from)
        date_to = self.request.query_params.get('date_to')
        if date_to:
            qs = qs.filter(inspection_date_plan__lte=date_to)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FileDownloadView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = GeneratedFile.objects.all()

    def retrieve(self, request, *args, **kwargs):
        file_obj = self.get_object()
        file_path = file_obj.file_path.path
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=file_obj.file_name,
            )
        return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
