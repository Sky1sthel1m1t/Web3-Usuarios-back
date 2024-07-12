from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.serializers import UserSerializer


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='login', url_name='login')
    def login(self, request):
        serializer = self.get_serializer(request.user)
        token = request.auth
        role_id = token['role']
        if role_id != 3:
            return Response(
                data={'detail': 'No tienes permisos para acceder a esta pagina'},
                status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)