from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from accounts.models import Account
from .models import LookupStatusCode, Terminal, Product, PowerOfAttorney
from .serializers import (
    LookupStatusCodeSerializer, TerminalSerializer,
    ProductSerializer, PowerOfAttorneySerializer,
)


class CanEditReferences(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        try:
            account = Account.objects.get(login=request.user.username)
        except Account.DoesNotExist:
            return False
        role = account.role_code
        if request.method == 'POST':
            return True
        if request.method in ('PUT', 'PATCH'):
            return role in ('manager', 'admin')
        if request.method == 'DELETE':
            return role == 'admin'
        return False


class LookupStatusCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LookupStatusCode.objects.all()
    serializer_class = LookupStatusCodeSerializer
    permission_classes = [IsAuthenticated]


class TerminalViewSet(viewsets.ModelViewSet):
    serializer_class = TerminalSerializer
    permission_classes = [CanEditReferences]

    def get_queryset(self):
        qs = Terminal.objects.select_related('owner_counterparty').order_by('terminal_name')
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(terminal_name__icontains=search)
        active_only = self.request.query_params.get('active_only', 'true')
        if active_only == 'true':
            qs = qs.filter(is_active=True)
        return qs


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [CanEditReferences]

    def get_queryset(self):
        qs = Product.objects.order_by('name_ru')
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name_ru__icontains=search)
        active_only = self.request.query_params.get('active_only', 'true')
        if active_only == 'true':
            qs = qs.filter(is_active=True)
        return qs


class PowerOfAttorneyViewSet(viewsets.ModelViewSet):
    serializer_class = PowerOfAttorneySerializer
    permission_classes = [CanEditReferences]

    def get_queryset(self):
        qs = PowerOfAttorney.objects.select_related(
            'principal_counterparty', 'attorney_account'
        ).order_by('-issue_date')
        active_only = self.request.query_params.get('active_only', 'true')
        if active_only == 'true':
            qs = qs.filter(is_active=True)
        counterparty_uuid = self.request.query_params.get('counterparty_uuid')
        if counterparty_uuid:
            qs = qs.filter(principal_counterparty__uuid=counterparty_uuid)
        return qs
