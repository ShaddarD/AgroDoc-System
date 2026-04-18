from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import Counterparty, Account
from .serializers import (
    CounterpartySerializer, AccountSerializer, AccountCreateSerializer,
    AccountUpdateSerializer, LoginSerializer, CurrentAccountSerializer,
    RegisterSerializer, SetPasswordSerializer,
)


def _issue_tokens(account: Account):
    """Get or create Django User for account and return JWT tokens + user data."""
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(username=account.login)
    user.first_name = account.first_name
    user.last_name = account.last_name
    user.email = account.email or ''
    user.is_staff = account.role_code == 'admin'
    user.is_active = True
    user.save(update_fields=['first_name', 'last_name', 'email', 'is_staff', 'is_active'])
    refresh = RefreshToken.for_user(user)
    return {
        'success': True,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': CurrentAccountSerializer(account).data,
    }


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


class CounterpartyViewSet(viewsets.ModelViewSet):
    permission_classes = [CanEditReferences]
    serializer_class = CounterpartySerializer

    def get_queryset(self):
        qs = Counterparty.objects.order_by('name_ru')
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name_ru__icontains=search)
        active_only = self.request.query_params.get('active_only', 'true')
        if active_only == 'true':
            qs = qs.filter(is_active=True)
        return qs


class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Account.objects.all().order_by('last_name', 'first_name')

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        if self.action in ('update', 'partial_update'):
            return AccountUpdateSerializer
        return AccountSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            account = Account.objects.select_related('counterparty').get(
                login=request.user.username
            )
        except Account.DoesNotExist:
            return Response({'detail': 'Аккаунт не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CurrentAccountSerializer(account).data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Check if account exists with empty password (first-login setup)
        try:
            account = Account.objects.get(login=username, is_active=True)
            if not account.password_hash:
                return Response({
                    'needs_password_setup': True,
                    'account_uuid': str(account.uuid),
                })
        except Account.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'success': False, 'message': 'Неверный логин или пароль'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            account = Account.objects.select_related('counterparty').get(login=username)
        except Account.DoesNotExist:
            account = getattr(user, '_account', None)

        return Response(_issue_tokens(account))


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        role_code = 'user'

        account = Account.objects.create(
            login=data['login'],
            password_hash=make_password(data['password']),
            role_code=role_code,
            last_name=data['last_name'],
            first_name=data['first_name'],
            middle_name=data.get('middle_name') or None,
            email=data.get('email') or None,
            phone=data.get('phone') or None,
            job_title=data.get('job_title') or None,
            counterparty=data['counterparty'],
            is_active=True,
        )
        account.refresh_from_db()
        return Response(_issue_tokens(account), status=status.HTTP_201_CREATED)


class SetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uuid = serializer.validated_data['uuid']
        password = serializer.validated_data['password']

        try:
            account = Account.objects.select_related('counterparty').get(uuid=uuid, is_active=True)
        except Account.DoesNotExist:
            return Response({'detail': 'Аккаунт не найден'}, status=status.HTTP_404_NOT_FOUND)

        if account.password_hash:
            return Response(
                {'detail': 'Пароль уже установлен'},
                status=status.HTTP_403_FORBIDDEN,
            )

        account.password_hash = make_password(password)
        account.save(update_fields=['password_hash'])
        return Response(_issue_tokens(account))


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'success': False, 'message': 'Refresh-токен не передан'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'message': 'Выход выполнен успешно'})


class InnLookupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        inn = request.query_params.get('inn', '').strip()
        if not inn:
            return Response({'error': 'Укажите ИНН'}, status=status.HTTP_400_BAD_REQUEST)

        from django.conf import settings
        token = getattr(settings, 'DADATA_TOKEN', '')
        if not token:
            return Response({'error': 'DADATA_TOKEN не настроен'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            import requests as req
            resp = req.post(
                'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party',
                json={'query': inn, 'count': 1},
                headers={'Authorization': f'Token {token}', 'Content-Type': 'application/json'},
                timeout=5,
            )
            suggestions = resp.json().get('suggestions', [])
            if suggestions:
                s = suggestions[0]
                return Response({
                    'name': s.get('value', ''),
                    'full_name': s.get('data', {}).get('name', {}).get('full_with_opf', ''),
                    'inn': s.get('data', {}).get('inn', inn),
                    'kpp': s.get('data', {}).get('kpp', ''),
                })
            return Response({'error': 'Компания не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ошибка запроса: {e}'}, status=status.HTTP_502_BAD_GATEWAY)
