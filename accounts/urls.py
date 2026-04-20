from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

router = DefaultRouter()
router.register(r'users', views.AccountViewSet, basename='account')
router.register(r'counterparties', views.CounterpartyViewSet, basename='counterparty')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('set-password/', views.SetPasswordView.as_view(), name='set-password'),
    path('inn-lookup/', views.InnLookupView.as_view(), name='inn-lookup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
