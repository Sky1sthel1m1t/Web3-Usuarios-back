from rest_framework.permissions import BasePermission


class IsAccessAdmin(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        group = request.user.groups.first()
        if group.name == 'Administrador de Accesos':
            return True


class IsRefineriaAdmin(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        group = request.user.groups.first()
        if group.name == 'Administrador de Refinería':
            return True


class IsSurtidorAdmin(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        group = request.user.groups.first()
        if group.name == 'Administrador de Surtidor':
            return True


class IsVendedor(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        group = request.user.groups.first()
        if group.name == 'Vendedor':
            return True


class IsChofer(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        group = request.user.groups.first()
        if group.name == 'Chofer':
            return True


class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
                handler
                and self.permission_classes_per_method
                and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)
