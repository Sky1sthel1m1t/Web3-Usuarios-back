from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.viewsets import UserViewSet, LoginViewSet, SurtidorViewSet

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'surtidores', SurtidorViewSet)
router.register('', LoginViewSet, basename='login')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]