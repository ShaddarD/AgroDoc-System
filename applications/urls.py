# applications/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),  # Главная страница
    path('files/<int:pk>/download/', views.FileDownloadView.as_view(), name='file-download'),
]