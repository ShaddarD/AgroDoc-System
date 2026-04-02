from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    ApplicationStatus, SenderRu, SenderPowerOfAttorney, Receiver,
    Gost, TrTs, TrTsSampling, Product, ProductPurpose, PackingType,
    Country, Representative, SamplingPlace, Laboratory, Certificate, Regulation,
)
from .serializers import (
    ApplicationStatusSerializer, SenderRuSerializer, SenderPowerOfAttorneySerializer,
    ReceiverSerializer, GostSerializer, TrTsSerializer, TrTsSamplingSerializer,
    ProductSerializer, ProductPurposeSerializer, PackingTypeSerializer,
    CountrySerializer, RepresentativeSerializer, SamplingPlaceSerializer,
    LaboratorySerializer, CertificateSerializer, RegulationSerializer,
)


class ApplicationStatusViewSet(viewsets.ModelViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated]


class SenderRuViewSet(viewsets.ModelViewSet):
    queryset = SenderRu.objects.filter(is_active=True)
    serializer_class = SenderRuSerializer
    permission_classes = [IsAuthenticated]


class SenderPowerOfAttorneyViewSet(viewsets.ModelViewSet):
    queryset = SenderPowerOfAttorney.objects.filter(is_active=True)
    serializer_class = SenderPowerOfAttorneySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        sender_id = self.request.query_params.get('sender_id')
        if sender_id:
            qs = qs.filter(sender_id=sender_id)
        return qs


class ReceiverViewSet(viewsets.ModelViewSet):
    queryset = Receiver.objects.filter(is_active=True)
    serializer_class = ReceiverSerializer
    permission_classes = [IsAuthenticated]


class GostViewSet(viewsets.ModelViewSet):
    queryset = Gost.objects.all()
    serializer_class = GostSerializer
    permission_classes = [IsAuthenticated]


class TrTsViewSet(viewsets.ModelViewSet):
    queryset = TrTs.objects.all()
    serializer_class = TrTsSerializer
    permission_classes = [IsAuthenticated]


class TrTsSamplingViewSet(viewsets.ModelViewSet):
    queryset = TrTsSampling.objects.all()
    serializer_class = TrTsSamplingSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductPurposeViewSet(viewsets.ModelViewSet):
    queryset = ProductPurpose.objects.all()
    serializer_class = ProductPurposeSerializer
    permission_classes = [IsAuthenticated]


class PackingTypeViewSet(viewsets.ModelViewSet):
    queryset = PackingType.objects.all()
    serializer_class = PackingTypeSerializer
    permission_classes = [IsAuthenticated]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


class RepresentativeViewSet(viewsets.ModelViewSet):
    queryset = Representative.objects.all()
    serializer_class = RepresentativeSerializer
    permission_classes = [IsAuthenticated]


class SamplingPlaceViewSet(viewsets.ModelViewSet):
    queryset = SamplingPlace.objects.all()
    serializer_class = SamplingPlaceSerializer
    permission_classes = [IsAuthenticated]


class LaboratoryViewSet(viewsets.ModelViewSet):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [IsAuthenticated]


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]


class RegulationViewSet(viewsets.ModelViewSet):
    queryset = Regulation.objects.all()
    serializer_class = RegulationSerializer
    permission_classes = [IsAuthenticated]
