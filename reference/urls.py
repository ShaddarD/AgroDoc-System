from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'statuses', views.LookupStatusCodeViewSet, basename='status')
router.register(r'terminals', views.TerminalViewSet, basename='terminal')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'powers-of-attorney', views.PowerOfAttorneyViewSet, basename='power-of-attorney')

urlpatterns = [
    path('', include(router.urls)),
]
