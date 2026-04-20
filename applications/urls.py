from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'applications', views.ApplicationViewSet, basename='application')
router.register(r'inspection-records', views.InspectionRecordViewSet, basename='inspection-record')

urlpatterns = [
    path('', include(router.urls)),
]
