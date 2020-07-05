from rest_framework.permissions import BasePermission


class IsClient(BasePermission):

    """
    Allows access only to clients providers
    """

    def has_permission(self, request, view):
        return request.user.filter(name='client').exists()


class IsServiceProvider(BasePermission):

    """
    Allows access only to service providers
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='service-provider').exists()
