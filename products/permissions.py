from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Разрешение на изменение только своих продуктов """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
