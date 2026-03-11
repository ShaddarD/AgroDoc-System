# accounts/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['patronymic', 'company_name', 'inn']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""

    full_name = serializers.SerializerMethodField()
    patronymic = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    inn = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name',
                  'patronymic', 'company_name', 'inn',
                  'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_patronymic(self, obj):
        return getattr(obj, 'profile', None) and obj.profile.patronymic or ''

    def get_company_name(self, obj):
        return getattr(obj, 'profile', None) and obj.profile.company_name or ''

    def get_inn(self, obj):
        return getattr(obj, 'profile', None) and obj.profile.inn or ''


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    patronymic = serializers.CharField(required=True, max_length=150)
    company_name = serializers.CharField(required=True, max_length=500)
    inn = serializers.CharField(required=False, allow_blank=True, max_length=12)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email',
                  'first_name', 'last_name', 'patronymic', 'company_name', 'inn']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        if not attrs.get('first_name', '').strip():
            raise serializers.ValidationError({"first_name": "Имя обязательно"})
        if not attrs.get('last_name', '').strip():
            raise serializers.ValidationError({"last_name": "Фамилия обязательна"})
        if not attrs.get('patronymic', '').strip():
            raise serializers.ValidationError({"patronymic": "Отчество обязательно"})
        if not attrs.get('company_name', '').strip():
            raise serializers.ValidationError({"company_name": "Наименование компании обязательно"})
        return attrs

    def create(self, validated_data):
        patronymic = validated_data.pop('patronymic')
        company_name = validated_data.pop('company_name')
        inn = validated_data.pop('inn', '')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            patronymic=patronymic,
            company_name=company_name,
            inn=inn,
        )
        return user
