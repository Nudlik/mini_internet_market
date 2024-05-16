from rest_framework import permissions


class IsEmailOwner(permissions.BasePermission):
    """ Разрешение, разрешающее редактировать только свой профиль. """

    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email
