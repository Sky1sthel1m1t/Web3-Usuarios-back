from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAccessAdmin, IsRefineriaAdmin
from api.serializers.serializers import UserSerializer, GroupWithIdSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsAccessAdmin
    ]

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def get_me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='roles')
    def get_roles(self, request):
        queryset = Group.objects.all()
        serializer = GroupWithIdSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='choferes',
            permission_classes=[IsAuthenticated, IsRefineriaAdmin])
    def get_choferes(self, request):
        queryset = User.objects.filter(groups__name='Chofer')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


