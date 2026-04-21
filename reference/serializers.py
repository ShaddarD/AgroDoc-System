from rest_framework import serializers
from .models import LookupStatusCode, Terminal, Product, PowerOfAttorney


class LookupStatusCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupStatusCode
        fields = ['status_code', 'description']


class TerminalSerializer(serializers.ModelSerializer):
    owner_counterparty_name = serializers.CharField(
        source='owner_counterparty.name_ru', read_only=True
    )

    class Meta:
        model = Terminal
        fields = [
            'uuid', 'terminal_code', 'terminal_name',
            'owner_counterparty', 'owner_counterparty_name',
            'address_ru', 'address_en', 'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'uuid', 'product_code', 'hs_code_tnved', 'name_ru', 'name_en',
            'botanical_name_latin', 'regulatory_documents',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class PowerOfAttorneySerializer(serializers.ModelSerializer):
    principal_counterparty_name = serializers.CharField(
        source='principal_counterparty.name_ru', read_only=True
    )
    attorney_counterparty_name = serializers.CharField(
        source='attorney_counterparty.name_ru', read_only=True
    )

    class Meta:
        model = PowerOfAttorney
        fields = [
            'uuid', 'poa_number', 'issue_date', 'validity_years', 'expiry_date',
            'principal_counterparty', 'principal_counterparty_name',
            'attorney_counterparty', 'attorney_counterparty_name',
            'status_code', 'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['uuid', 'expiry_date', 'created_at', 'updated_at']
