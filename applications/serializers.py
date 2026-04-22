from rest_framework import serializers

from .models import Application, InspectionRecord
from reference.models import LookupStatusCode, Terminal, Product, PowerOfAttorney
from accounts.models import Counterparty, Account


class ApplicationListSerializer(serializers.ModelSerializer):
    status_code = serializers.CharField(source='status_id', read_only=True)
    applicant_counterparty_name = serializers.CharField(
        source='applicant_counterparty.name_ru', read_only=True,
    )
    terminal_name = serializers.CharField(source='terminal.terminal_name', read_only=True)
    product_name = serializers.CharField(source='product.name_ru', read_only=True)

    class Meta:
        model = Application
        fields = [
            'uuid',
            'application_number',
            'application_type_code',
            'status_code',
            'applicant_counterparty',
            'applicant_counterparty_name',
            'terminal',
            'terminal_name',
            'product',
            'product_name',
            'planned_inspection_date',
            'weight_mt',
            'submitted_at',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class ApplicationReadSerializer(serializers.ModelSerializer):
    status_code = serializers.CharField(source='status_id', read_only=True)
    status_description = serializers.CharField(source='status.description', read_only=True)

    terminal_name = serializers.CharField(source='terminal.terminal_name', read_only=True)
    product_name_ru = serializers.CharField(source='product.name_ru', read_only=True)
    product_name_en_ref = serializers.CharField(source='product.name_en', read_only=True)
    power_of_attorney_number = serializers.CharField(source='power_of_attorney.poa_number', read_only=True)

    applicant_counterparty_name = serializers.CharField(
        source='applicant_counterparty.name_ru',
        read_only=True,
    )
    applicant_account_email = serializers.CharField(
        source='applicant_account.email',
        read_only=True,
    )

    master_application_number = serializers.CharField(
        source='master_application.application_number',
        read_only=True,
    )

    class Meta:
        model = Application
        fields = [
            'uuid',
            'application_number',
            'application_type_code',

            'status_code',
            'status_description',

            'applicant_counterparty',
            'applicant_counterparty_name',
            'applicant_account',
            'applicant_account_email',

            'terminal',
            'terminal_name',
            'product',
            'product_name_ru',
            'product_name_en_ref',
            'power_of_attorney',
            'power_of_attorney_number',

            'master_application',
            'master_application_number',
            'stuffing_act_uuid',

            'sender_en_manual',
            'product_name_en_manual',
            'contract_number_manual',
            'contract_date_manual',
            'discharge_port_ru_manual',
            'discharge_port_en_manual',
            'additional_declaration',
            'notes',
            'harvest_year',
            'manufacture_date',
            'weight_mt',
            'planned_inspection_date',
            'planned_inspection_time',

            'ikr_number',
            'ikr_date',
            'asid_number',
            'is_on_behalf',
            'need_color_letter',

            'submitted_at',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class ApplicationCreateSerializer(serializers.Serializer):
    application_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    application_type_code = serializers.ChoiceField(
        choices=[choice[0] for choice in Application.TYPE_CHOICES],
        required=False,
        default=Application.TYPE_VNIIKR,
    )

    applicant_counterparty_uuid = serializers.UUIDField(required=False, allow_null=True)
    applicant_account_uuid = serializers.UUIDField(required=False, allow_null=True)

    terminal_uuid = serializers.UUIDField(required=False, allow_null=True)
    product_uuid = serializers.UUIDField(required=False, allow_null=True)
    power_of_attorney_uuid = serializers.UUIDField(required=False, allow_null=True)

    status_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    master_application_uuid = serializers.UUIDField(required=False, allow_null=True)
    stuffing_act_uuid = serializers.UUIDField(required=False, allow_null=True)

    sender_en_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    product_name_en_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    contract_number_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    contract_date_manual = serializers.DateField(required=False, allow_null=True)

    discharge_port_ru_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    discharge_port_en_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    additional_declaration = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    harvest_year = serializers.IntegerField(required=False, allow_null=True)
    manufacture_date = serializers.DateField(required=False, allow_null=True)

    weight_mt = serializers.DecimalField(
        max_digits=14,
        decimal_places=3,
        required=False,
        allow_null=True,
    )

    planned_inspection_date = serializers.DateField(required=False, allow_null=True)
    planned_inspection_time = serializers.TimeField(required=False, allow_null=True)

    ikr_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ikr_date = serializers.DateField(required=False, allow_null=True)
    asid_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    is_on_behalf = serializers.BooleanField(required=False, default=False)
    need_color_letter = serializers.BooleanField(required=False, default=False)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_status_code(self, value):
        if value in (None, ''):
            return None
        if not LookupStatusCode.objects.filter(status_code=value).exists():
            raise serializers.ValidationError('Указан несуществующий status_code.')
        return value

    def validate_terminal_uuid(self, value):
        if value and not Terminal.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий terminal_uuid.')
        return value

    def validate_product_uuid(self, value):
        if value and not Product.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий product_uuid.')
        return value

    def validate_power_of_attorney_uuid(self, value):
        if value and not PowerOfAttorney.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий power_of_attorney_uuid.')
        return value

    def validate_applicant_counterparty_uuid(self, value):
        if value and not Counterparty.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий applicant_counterparty_uuid.')
        return value

    def validate_applicant_account_uuid(self, value):
        if value and not Account.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий applicant_account_uuid.')
        return value

    def validate_master_application_uuid(self, value):
        if value and not Application.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указана несуществующая master_application_uuid.')
        return value

    def validate(self, attrs):
        # Contract: ikr_number requires ikr_date (format contract, not domain rule)
        if attrs.get('ikr_number') and not attrs.get('ikr_date'):
            raise serializers.ValidationError({
                'ikr_date': 'Если указан ИКР, нужно указать дату ИКР.'
            })
        return attrs


class ApplicationUpdateSerializer(serializers.Serializer):
    application_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    application_type_code = serializers.ChoiceField(
        choices=[choice[0] for choice in Application.TYPE_CHOICES],
        required=False,
    )

    applicant_counterparty_uuid = serializers.UUIDField(required=False, allow_null=True)
    applicant_account_uuid = serializers.UUIDField(required=False, allow_null=True)

    terminal_uuid = serializers.UUIDField(required=False, allow_null=True)
    product_uuid = serializers.UUIDField(required=False, allow_null=True)
    power_of_attorney_uuid = serializers.UUIDField(required=False, allow_null=True)

    status_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    master_application_uuid = serializers.UUIDField(required=False, allow_null=True)
    stuffing_act_uuid = serializers.UUIDField(required=False, allow_null=True)

    sender_en_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    product_name_en_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    contract_number_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    contract_date_manual = serializers.DateField(required=False, allow_null=True)

    discharge_port_ru_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    discharge_port_en_manual = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    additional_declaration = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    harvest_year = serializers.IntegerField(required=False, allow_null=True)
    manufacture_date = serializers.DateField(required=False, allow_null=True)

    weight_mt = serializers.DecimalField(
        max_digits=14,
        decimal_places=3,
        required=False,
        allow_null=True,
    )

    planned_inspection_date = serializers.DateField(required=False, allow_null=True)
    planned_inspection_time = serializers.TimeField(required=False, allow_null=True)

    ikr_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ikr_date = serializers.DateField(required=False, allow_null=True)
    asid_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    is_on_behalf = serializers.BooleanField(required=False)
    need_color_letter = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_status_code(self, value):
        if value in (None, ''):
            return None
        if not LookupStatusCode.objects.filter(status_code=value).exists():
            raise serializers.ValidationError('Указан несуществующий status_code.')
        return value

    def validate_terminal_uuid(self, value):
        if value and not Terminal.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий terminal_uuid.')
        return value

    def validate_product_uuid(self, value):
        if value and not Product.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий product_uuid.')
        return value

    def validate_power_of_attorney_uuid(self, value):
        if value and not PowerOfAttorney.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий power_of_attorney_uuid.')
        return value

    def validate_applicant_counterparty_uuid(self, value):
        if value and not Counterparty.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий applicant_counterparty_uuid.')
        return value

    def validate_applicant_account_uuid(self, value):
        if value and not Account.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указан несуществующий applicant_account_uuid.')
        return value

    def validate_master_application_uuid(self, value):
        if value and not Application.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Указана несуществующая master_application_uuid.')
        return value

    def validate(self, attrs):
        if attrs.get('ikr_number') and not attrs.get('ikr_date'):
            raise serializers.ValidationError({
                'ikr_date': 'Если указан ИКР, нужно указать дату ИКР.'
            })
        return attrs


class InspectionRecordSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source='application.application_number',
        read_only=True,
    )
    created_by_email = serializers.CharField(
        source='created_by.email',
        read_only=True,
    )

    class Meta:
        model = InspectionRecord
        fields = [
            'id',
            'number',
            'client',
            'manager',
            'commodity',
            'container_count',
            'container_type',
            'weight',
            'pod',
            'terminal',
            'quarantine',
            'inspection_date_plan',
            'fss_date_plan',
            'cargo_status',
            'documents_status',
            'comments',
            'application',
            'application_number',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
