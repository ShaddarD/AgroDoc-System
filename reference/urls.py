# reference/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'applicants', views.ApplicantViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'importers', views.ImporterViewSet)
router.register(r'inspection-places', views.InspectionPlaceViewSet)
router.register(r'packing-types', views.PackingTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]