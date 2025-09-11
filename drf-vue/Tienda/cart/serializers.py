from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer
from products.models import Product, Color, Talle
from products.serializers import ColorSerializer, TalleSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True, allow_null=True, required=False
    )
    talle = TalleSerializer(read_only=True)
    talle_id = serializers.PrimaryKeyRelatedField(
        queryset=Talle.objects.all(), source='talle', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'color', 'color_id', 'talle', 'talle_id', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'completed', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            item = CartItem.objects.create(**item_data)
            cart.items.add(item)
        return cart
