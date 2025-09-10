from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
