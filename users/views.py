from djoser import views


class OverrideMethodsMeta(type):
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
    pass
