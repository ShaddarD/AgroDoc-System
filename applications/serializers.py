from rest_framework import serializers
from .models import (
    Application, ApplicationContainer, ApplicationCertificate,
    ApplicationRegulation, GeneratedFile, InspectionRecord, ApplicationHistory,
)
from reference.serializers import (
    ApplicationStatusSerializer, SenderRuSerializer, SenderPowerOfAttorneySerializer,
    ReceiverSerializer, ProductSerializer, ProductPurposeSerializer,
    PackingTypeSerializer, CountrySerializer, RepresentativeSerializer,
    SamplingPlaceSerializer, LaboratorySerializer, CertificateSerializer,
    RegulationSerializer,
)


class ApplicationContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationContainer
        fields = ['id', 'container_number', 'sort_order']


class ApplicationCertificateSerializer(serializers.ModelSerializer):
    certificate_detail = CertificateSerializer(source='certificate', read_only=True)

    class Meta:
        model = ApplicationCertificate
        fields = ['id', 'certificate', 'certificate_detail', 'copies_count', 'is_required']


class ApplicationRegulationSerializer(serializers.ModelSerializer):
    regulation_detail = RegulationSerializer(source='regulation', read_only=True)

    class Meta:
        model = ApplicationRegulation
        fields = ['id', 'regulation', 'regulation_detail', 'comment']


class ApplicationListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    status_code = serializers.CharField(source='status.code', read_only=True)
    sender_name = serializers.CharField(source='sender_ru.name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.name_en', read_only=True)
    product_name = serializers.CharField(source='product.name_ru', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'application_number', 'created_at', 'updated_at',
            'status', 'status_name', 'status_code',
            'sender_name', 'receiver_name', 'product_name',
            'weight_mt', 'planned_inspection_date', 'created_by_name',
        ]


class ApplicationDetailSerializer(serializers.ModelSerializer):
    status_detail = ApplicationStatusSerializer(source='status', read_only=True)
    sender_ru_detail = SenderRuSerializer(source='sender_ru', read_only=True)
    sender_power_of_attorney_detail = SenderPowerOfAttorneySerializer(
        source='sender_power_of_attorney', read_only=True
    )
    receiver_detail = ReceiverSerializer(source='receiver', read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)
    purpose_detail = ProductPurposeSerializer(source='purpose', read_only=True)
    packing_type_detail = PackingTypeSerializer(source='packing_type', read_only=True)
    import_country_detail = CountrySerializer(source='import_country', read_only=True)
    representative_detail = RepresentativeSerializer(source='representative', read_only=True)
    sampling_place_detail = SamplingPlaceSerializer(source='sampling_place', read_only=True)
    laboratory_detail = LaboratorySerializer(source='laboratory', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    containers = ApplicationContainerSerializer(many=True, read_only=True)
    certificates = ApplicationCertificateSerializer(many=True, read_only=True)
    regulations = ApplicationRegulationSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['application_number', 'created_at', 'updated_at', 'created_by']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['application_number', 'created_at', 'updated_at', 'created_by']


class GeneratedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedFile
        fields = ['id', 'file_name', 'file_path', 'file_type', 'created_at']


class InspectionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class ApplicationHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = ApplicationHistory
        fields = ['id', 'user', 'user_name', 'action', 'changes', 'created_at']
