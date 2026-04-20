from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Application, InspectionRecord
from .serializers import (
    ApplicationListSerializer, ApplicationDetailSerializer,
    ApplicationCreateSerializer, InspectionRecordSerializer,
)


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        if self.action in ('create',):
            return ApplicationCreateSerializer
        return ApplicationDetailSerializer

    def get_queryset(self):
        qs = Application.objects.select_related(
            'applicant_counterparty', 'applicant_account',
            'terminal', 'product', 'power_of_attorney',
        ).filter(is_active=True)

        status_code = self.request.query_params.get('status')
        if status_code:
            qs = qs.filter(status_code=status_code)

        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(application_number__icontains=search) |
                Q(product__name_ru__icontains=search) |
                Q(applicant_counterparty__name_ru__icontains=search)
            ).distinct()

        date_from = self.request.query_params.get('date_from')
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class InspectionRecordViewSet(viewsets.ModelViewSet):
    serializer_class = InspectionRecordSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = InspectionRecord.objects.all()
        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(client__icontains=search) |
                Q(commodity__icontains=search) |
                Q(container_count__icontains=search)
            )
        return qs

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user)
