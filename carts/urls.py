from django.urls import include, path
from rest_framework.routers import DefaultRouter

from carts.views import CartViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls)),
]
