from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'statuses', views.ApplicationStatusViewSet, basename='status')
router.register(r'senders', views.SenderRuViewSet, basename='sender')
router.register(r'powers-of-attorney', views.SenderPowerOfAttorneyViewSet, basename='power-of-attorney')
router.register(r'receivers', views.ReceiverViewSet, basename='receiver')
router.register(r'gosts', views.GostViewSet, basename='gost')
router.register(r'tr-ts', views.TrTsViewSet, basename='tr-ts')
router.register(r'tr-ts-sampling', views.TrTsSamplingViewSet, basename='tr-ts-sampling')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'purposes', views.ProductPurposeViewSet, basename='purpose')
router.register(r'packing-types', views.PackingTypeViewSet, basename='packing-type')
router.register(r'countries', views.CountryViewSet, basename='country')
router.register(r'representatives', views.RepresentativeViewSet, basename='representative')
router.register(r'sampling-places', views.SamplingPlaceViewSet, basename='sampling-place')
router.register(r'laboratories', views.LaboratoryViewSet, basename='laboratory')
router.register(r'certificates', views.CertificateViewSet, basename='certificate')
router.register(r'regulations', views.RegulationViewSet, basename='regulation')

urlpatterns = [
    path('', include(router.urls)),
]
