# accounts/views.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CurrentUserView(APIView):
    """Получение информации о текущем пользователе"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LoginView(APIView):
    """Вход в систему — возвращает JWT токены"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data,
                    'message': 'Вход выполнен успешно'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Неверное имя пользователя или пароль'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Выход из системы — инвалидирует refresh токен"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'success': True, 'message': 'Выход выполнен успешно'})


class InnLookupView(APIView):
    """Поиск компании по ИНН через DaData API"""
    permission_classes = [AllowAny]

    def get(self, request):
        inn = request.query_params.get('inn', '').strip()
        if not inn:
            return Response({'error': 'Укажите ИНН'}, status=status.HTTP_400_BAD_REQUEST)

        from django.conf import settings
        token = getattr(settings, 'DADATA_TOKEN', '')
        if not token:
            return Response({'error': 'DADATA_TOKEN не настроен в settings.py'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            import requests as req
            resp = req.post(
                'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party',
                json={'query': inn, 'count': 1},
                headers={
                    'Authorization': f'Token {token}',
                    'Content-Type': 'application/json',
                },
                timeout=5,
            )
            data = resp.json()
            suggestions = data.get('suggestions', [])
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
            return Response({'error': f'Ошибка запроса: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)


class RegisterView(APIView):
    """Регистрация нового пользователя (только для администраторов)"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'message': 'Пользователь успешно создан'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
