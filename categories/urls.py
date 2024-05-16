from django.urls import include, path
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]
