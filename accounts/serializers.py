from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Counterparty, Account


class CounterpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = [
            'uuid', 'name_ru', 'name_en', 'inn', 'kpp', 'ogrn',
            'legal_address_ru', 'actual_address_ru', 'legal_address_en', 'actual_address_en',
            'status_code', 'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class AccountSerializer(serializers.ModelSerializer):
    counterparty = CounterpartySerializer(read_only=True)
    counterparty_name = serializers.CharField(source='counterparty.name_ru', read_only=True)

    class Meta:
        model = Account
        fields = [
            'uuid', 'login', 'role_code', 'last_name', 'first_name', 'middle_name',
            'counterparty', 'counterparty_name', 'phone', 'email', 'job_title',
            'permissions', 'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class AccountCreateSerializer(serializers.ModelSerializer):
    """Admin panel — password is optional; if omitted, user sets it on first login."""
    password = serializers.CharField(write_only=True, required=False, min_length=6, allow_blank=True)

    class Meta:
        model = Account
        fields = [
            'login', 'password', 'role_code', 'last_name', 'first_name', 'middle_name',
            'counterparty', 'phone', 'email', 'job_title',
        ]
        extra_kwargs = {
            'counterparty': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['password_hash'] = make_password(password) if password else ''
        return Account.objects.create(**validated_data)


class AccountUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6, allow_blank=True)

    class Meta:
        model = Account
        fields = [
            'role_code', 'last_name', 'first_name', 'middle_name',
            'counterparty', 'phone', 'email', 'job_title',
            'permissions', 'is_active', 'password',
        ]
        extra_kwargs = {
            'counterparty': {'required': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    last_name = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)
    job_title = serializers.CharField(max_length=150, required=False, allow_blank=True)
    counterparty = serializers.PrimaryKeyRelatedField(queryset=Counterparty.objects.all(), required=True)

    def validate_login(self, value):
        if Account.objects.filter(login=value).exists():
            raise serializers.ValidationError('Этот логин уже занят')
        return value

    def validate_email(self, value):
        if value and Account.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('Этот email уже используется')
        return value.lower() if value else value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают'})
        return attrs


class SetPasswordSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают'})
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class CurrentAccountSerializer(serializers.ModelSerializer):
    counterparty = CounterpartySerializer(read_only=True)

    class Meta:
        model = Account
        fields = [
            'uuid', 'login', 'role_code', 'last_name', 'first_name', 'middle_name',
            'counterparty', 'phone', 'email', 'job_title', 'permissions', 'is_active',
        ]
