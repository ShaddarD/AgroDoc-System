# applications/serializers.py

from rest_framework import serializers
from .models import Application, GeneratedFile
from reference.models import Applicant, Product, Importer, InspectionPlace

class ApplicantSerializer(serializers.ModelSerializer):
    """Сериализатор для заявителя"""
    class Meta:
        model = Applicant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукции"""
    class Meta:
        model = Product
        fields = '__all__'

class ImporterSerializer(serializers.ModelSerializer):
    """Сериализатор для импортера"""
    class Meta:
        model = Importer
        fields = '__all__'

class InspectionPlaceSerializer(serializers.ModelSerializer):
    """Сериализатор для места инспекции"""
    class Meta:
        model = InspectionPlace
        fields = '__all__'

class ApplicationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заявок"""
    
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    product_name = serializers.SerializerMethodField()
    importer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'application_number', 'created_at', 'status',
            'created_by_name', 'product_name', 'importer_name',
            'weight_tons', 'weight_mt'
        ]
    
    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name_rus
        return obj.product_rus
    
    def get_importer_name(self, obj):
        if obj.importer:
            return obj.importer.name_eng
        return obj.importer_name_eng

class ApplicationDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации"""
    
    applicant_data = ApplicantSerializer(source='applicant', read_only=True)
    product_data = ProductSerializer(source='product', read_only=True)
    importer_data = ImporterSerializer(source='importer', read_only=True)
    inspection_place_data = InspectionPlaceSerializer(source='inspection_place', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['application_number', 'created_at', 'updated_at']

class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки"""
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['application_number', 'created_at', 'updated_at']

class GeneratedFileSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов"""
    
    class Meta:
        model = GeneratedFile
        fields = ['id', 'file_name', 'file_path', 'file_type', 'created_at']