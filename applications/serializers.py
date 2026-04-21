from rest_framework import serializers
from .models import Application, InspectionRecord
from accounts.serializers import CounterpartySerializer, AccountSerializer
from reference.serializers import TerminalSerializer, ProductSerializer, PowerOfAttorneySerializer


class ApplicationListSerializer(serializers.ModelSerializer):
    applicant_counterparty_name = serializers.CharField(
        source='applicant_counterparty.name_ru', read_only=True
    )
    terminal_name = serializers.CharField(source='terminal.terminal_name', read_only=True)
    product_name = serializers.CharField(source='product.name_ru', read_only=True)

    class Meta:
        model = Application
        fields = [
            'uuid', 'application_number', 'status_code',
            'applicant_counterparty', 'applicant_counterparty_name',
            'terminal', 'terminal_name',
            'product', 'product_name',
            'submitted_at', 'is_active', 'created_at', 'updated_at',
        ]


class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant_counterparty = CounterpartySerializer(read_only=True)
    applicant_account = AccountSerializer(read_only=True)
    terminal = TerminalSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    power_of_attorney = PowerOfAttorneySerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'uuid', 'application_number', 'status_code',
            'applicant_counterparty', 'applicant_account',
            'terminal', 'product', 'power_of_attorney',
            'submitted_at', 'notes', 'is_active', 'created_at', 'updated_at',
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'applicant_counterparty', 'applicant_account',
            'terminal', 'product', 'power_of_attorney',
            'status_code', 'notes',
        ]

    def validate(self, attrs):
        from accounts.models import Counterparty, Account
        from reference.models import Terminal, Product, PowerOfAttorney

        for field, model in [
            ('applicant_counterparty', Counterparty),
            ('applicant_account', Account),
            ('terminal', Terminal),
            ('product', Product),
        ]:
            val = attrs.get(field)
            if val and not model.objects.filter(pk=val.pk).exists():
                raise serializers.ValidationError({field: 'Запись не найдена'})
        return attrs


class InspectionRecordSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source='application.application_number', read_only=True
    )

    class Meta:
        model = InspectionRecord
        fields = [
            'id', 'number', 'client', 'manager', 'commodity',
            'container_count', 'container_type', 'weight', 'pod', 'terminal',
            'quarantine', 'inspection_date_plan', 'fss_date_plan',
            'cargo_status', 'documents_status', 'comments',
            'application', 'application_number',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'application_number', 'created_at', 'updated_at']
