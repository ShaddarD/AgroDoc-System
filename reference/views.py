# reference/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Applicant, Product, Importer, InspectionPlace, PackingType
from applications.serializers import (
    ApplicantSerializer, ProductSerializer, 
    ImporterSerializer, InspectionPlaceSerializer
)

# Создаем отдельный сериализатор для PackingType, так как его нет в applications.serializers
from rest_framework import serializers

class PackingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingType
        fields = '__all__'

class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.filter(is_active=True)
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ImporterViewSet(viewsets.ModelViewSet):
    queryset = Importer.objects.filter(is_active=True)
    serializer_class = ImporterSerializer
    permission_classes = [IsAuthenticated]

class InspectionPlaceViewSet(viewsets.ModelViewSet):
    queryset = InspectionPlace.objects.filter(is_active=True)
    serializer_class = InspectionPlaceSerializer
    permission_classes = [IsAuthenticated]

class PackingTypeViewSet(viewsets.ModelViewSet):
    queryset = PackingType.objects.all()
    serializer_class = PackingTypeSerializer
    permission_classes = [IsAuthenticated]