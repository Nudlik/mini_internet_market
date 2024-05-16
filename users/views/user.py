from djoser import views
from djoser.serializers import UserCreateSerializer
from rest_framework.permissions import AllowAny, IsAdminUser

from users.permissions import IsEmailOwner


class OverrideMethodsMeta(type):
    """ Перегружаю методы класса юзер-джосера, не по СОЛИД, но создатели библиотеки сделали не модульный код :( """

    set_none = {
        'activation',
        'resend_activation',
        'set_username',
        'reset_username',
        'reset_username_confirm',
    }

    def __new__(mcs, name, bases, dct):
        for base in bases:
            for attr_name in dir(base):
                attr = getattr(base, attr_name)
                if callable(attr) and not attr_name.startswith("__") and attr_name in mcs.set_none:
                    dct[attr_name] = lambda self, *args, **kwargs: None
        return super().__new__(mcs, name, bases, dct)


class UserViewSet(views.UserViewSet, metaclass=OverrideMethodsMeta):
    perms_methods = {
        'create': [AllowAny],
        'update': [IsEmailOwner | IsAdminUser],
        'partial_update': [IsEmailOwner | IsAdminUser],
        'destroy': [IsEmailOwner | IsAdminUser],
    }
    choice_serializer = {
        'create': UserCreateSerializer,
    }

    def get_permissions(self):
        if (permission_ := self.perms_methods.get(self.action)) is None:
            return super().get_permissions()
        return [permission() for permission in permission_]

    def get_serializer_class(self):
        if (serializer := self.choice_serializer.get(self.action)) is None:
            return super().get_serializer_class()
        return serializer
