from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Account


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


def make_section_permission(section: str):
    """Returns a DRF permission class that allows admins unconditionally,
    and other users only if `section` is in their permissions array."""
    class _SectionPermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False
            try:
                account = Account.objects.get(login=request.user.username)
            except Account.DoesNotExist:
                return False
            return account.role_code == 'admin' or section in (account.permissions or [])
    _SectionPermission.__name__ = f'SectionPermission_{section}'
    return _SectionPermission
