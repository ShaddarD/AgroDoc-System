from rest_framework import serializers
from .models import (
    ApplicationStatus, SenderRu, SenderPowerOfAttorney, Receiver,
    Gost, TrTs, TrTsSampling, Product, ProductPurpose, PackingType,
    Country, Representative, SamplingPlace, Laboratory, Certificate, Regulation,
)


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'


class SenderRuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderRu
        fields = '__all__'


class SenderPowerOfAttorneySerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderPowerOfAttorney
        fields = '__all__'


class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = '__all__'


class GostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gost
        fields = '__all__'


class TrTsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrTs
        fields = '__all__'


class TrTsSamplingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrTsSampling
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPurpose
        fields = '__all__'


class PackingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingType
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = '__all__'


class SamplingPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingPlace
        fields = '__all__'


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class RegulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regulation
        fields = '__all__'
