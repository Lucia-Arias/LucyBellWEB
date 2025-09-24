from rest_framework import serializers
from .models import Order
from cart.serializers import CartSerializer
from cart.models import Cart

class OrderSerializer(serializers.ModelSerializer):
    carrito = CartSerializer(read_only=True)
    carrito_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), source="carrito", write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id", "cliente_nombre", "cliente_telefono",
            "metodo_envio", "metodo_pago",
            "opcion_entrega", "fecha_entrega",
            "carrito", "carrito_id",
            "creado_en", "completado", "total"
        ]
