from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, InspectionRecordViewSet

router = DefaultRouter()
router.register(r'', ApplicationViewSet, basename='application')
router.register(r'inspection-records', InspectionRecordViewSet, basename='inspection-record')

urlpatterns = [
    path('', include(router.urls)),
]