from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Surtidor
from api.permissions import IsAccessAdmin
from api.serializers import SurtidorSerializer, UserSerializer
from api.serializers.serializers import SurtidorWithoutUsersSerializer


class SurtidorViewSet(viewsets.ModelViewSet):
    queryset = Surtidor.objects.all()
    serializer_class = SurtidorSerializer
    permission_classes = [
        IsAuthenticated,
        IsAccessAdmin
    ]

    def list(self, request, *args, **kwargs):
        queryset = Surtidor.objects.all()
        serializer = SurtidorWithoutUsersSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, IsAccessAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='usuarios-disponibles')
    def get_surtidor_users(self, request):
        queryset = User.objects.filter(groups__name__in=['Vendedor', 'Administrador de Surtidor']).filter(
            surtidor_usuarios=None)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)