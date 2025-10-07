from rest_framework import serializers
from .models import Category, Material, Product, Color, Talle, ProductoTalle, ProductoColor

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class TalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talle
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    material_name = serializers.ReadOnlyField(source='material.name')
    # Campos de solo lectura para mostrar información relacionada
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    talle_name = serializers.CharField(source='talle.name', read_only=True)

    # Campo calculado de stock total
    total_stock = serializers.SerializerMethodField()
    
    # Nuevos campos para talles y colores disponibles
    talles_disponibles = serializers.SerializerMethodField()
    colores_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_total_stock(self, obj):
        # Suma de stocks de todos los talles y colores
        stock_talles = sum(pt.stock for pt in obj.productotalle_set.all())
        stock_colores = sum(pc.stock for pc in obj.productocolor_set.all())
        return max(stock_talles, stock_colores, 0)
    
    def get_talles_disponibles(self, obj):
        # Obtener talles que tienen stock > 0
        talles_con_stock = ProductoTalle.objects.filter(
            producto=obj, 
            stock__gt=0
        ).select_related('talle')
        return [pt.talle.name for pt in talles_con_stock]
    
    def get_colores_disponibles(self, obj):
        # Obtener colores que tienen stock > 0
        colores_con_stock = ProductoColor.objects.filter(
            producto=obj, 
            stock__gt=0
        ).select_related('color')
        return [pc.color.name for pc in colores_con_stock]

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    talle_name = serializers.CharField(source='talle.name', read_only=True)
    total_stock = serializers.SerializerMethodField()
    
    # Nuevos campos para talles y colores disponibles
    talles_disponibles = serializers.SerializerMethodField()
    colores_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'category', 'category_name', 
            'material', 'material_name', 'color', 'color_name',
            'talle', 'talle_name', 'price', 'sale_price', 'total_stock',
            'talles_disponibles', 'colores_disponibles'  # Agregados aquí
        ]

    def get_total_stock(self, obj):
        stock_talles = sum(pt.stock for pt in obj.productotalle_set.all())
        stock_colores = sum(pc.stock for pc in obj.productocolor_set.all())
        return max(stock_talles, stock_colores, 0)
    
    def get_talles_disponibles(self, obj):
        # Obtener talles que tienen stock > 0
        talles_con_stock = ProductoTalle.objects.filter(
            producto=obj, 
            stock__gt=0
        ).select_related('talle')
        return [pt.talle.name for pt in talles_con_stock]
    
    def get_colores_disponibles(self, obj):
        # Obtener colores que tienen stock > 0
        colores_con_stock = ProductoColor.objects.filter(
            producto=obj, 
            stock__gt=0
        ).select_related('color')
        return [pc.color.name for pc in colores_con_stock]