from django.urls import include, path
from rest_framework.routers import DefaultRouter

from carts import apps
from carts.views import CartViewSet, webhook, success, canceled

app_name = apps.CartsConfig.name

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='carts')

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path('buy/success/', success, name='success'),
    path('buy/canceled/', canceled, name='canceled'),

    path('', include(router.urls)),
]
