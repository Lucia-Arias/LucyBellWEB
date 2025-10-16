from rest_framework import serializers
from .models import Category, Material, Product, Color, Talle, ProductoTalle, ProductoColor, ProductImage

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

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order', 'alt_text']

# serializers.py
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    material_name = serializers.ReadOnlyField(source='material.name')
    color_name = serializers.CharField(source='color.name', read_only=True, allow_null=True)
    talle_name = serializers.CharField(source='talle.name', read_only=True, allow_null=True)

    # Campo calculado de stock total
    total_stock = serializers.SerializerMethodField()
    
    # Nuevos campos para talles y colores disponibles
    talles_disponibles = serializers.SerializerMethodField()
    colores_disponibles = serializers.SerializerMethodField()

    # Lista de todas las imágenes
    images = ProductImageSerializer(many=True, read_only=True)

    # Campos adicionales
    is_on_sale = serializers.ReadOnlyField()
    profit_margin = serializers.ReadOnlyField()
    etiqueta = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'price_cost', 'sale_price',
            'category', 'category_name', 'material', 'material_name', 
            'color', 'color_name', 'talle', 'talle_name', 'fecha_creacion',
            'total_stock', 'talles_disponibles', 'colores_disponibles',
            'images', 'is_on_sale', 'profit_margin', 'etiqueta'
        ]

    def get_total_stock(self, obj):
        """Calcula el stock total basado en ProductoTalle"""
        try:
            stock_total = sum(pt.stock for pt in ProductoTalle.objects.filter(producto=obj))
            return stock_total
        except:
            return 0
    
    def get_talles_disponibles(self, obj):
        """Obtiene talles que tienen stock > 0"""
        try:
            talles_con_stock = ProductoTalle.objects.filter(
                producto=obj, 
                stock__gt=0
            ).select_related('talle')
            return [{"talle": pt.talle.name, "stock": pt.stock} for pt in talles_con_stock]
        except:
            return []
    
    def get_colores_disponibles(self, obj):
        """Obtiene colores que tienen stock > 0"""
        try:
            colores_con_stock = ProductoColor.objects.filter(
                producto=obj, 
                stock__gt=0
            ).select_related('color')
            return [{"color": pc.color.name, "stock": pc.stock} for pc in colores_con_stock]
        except:
            return []

    def get_etiqueta(self, obj):
        """Devuelve la etiqueta del producto"""
        return obj.calcular_etiqueta()

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True, allow_null=True)
    talle_name = serializers.CharField(source='talle.name', read_only=True, allow_null=True)
    total_stock = serializers.SerializerMethodField()
    
    # Nuevos campos para talles y colores disponibles
    talles_disponibles = serializers.SerializerMethodField()
    colores_disponibles = serializers.SerializerMethodField()

    # Campo para compatibilidad (imagen principal)
    image = serializers.SerializerMethodField()

    # Campos adicionales para la lista
    is_on_sale = serializers.ReadOnlyField()
    etiqueta = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'category', 'category_name', 
            'material', 'material_name', 'color', 'color_name',
            'talle', 'talle_name', 'price', 'sale_price', 'total_stock',
            'talles_disponibles', 'colores_disponibles', 'is_on_sale', 'etiqueta',
            'fecha_creacion'
        ]

    def get_image(self, obj):
        """Devuelve la imagen principal para compatibilidad"""
        return obj.main_image

    def get_total_stock(self, obj):
        """Calcula el stock total basado en ProductoTalle"""
        try:
            stock_total = sum(pt.stock for pt in ProductoTalle.objects.filter(producto=obj))
            return stock_total
        except:
            return 0
    
    def get_talles_disponibles(self, obj):
        """Obtiene talles que tienen stock > 0"""
        try:
            talles_con_stock = ProductoTalle.objects.filter(
                producto=obj, 
                stock__gt=0
            ).select_related('talle')
            return [pt.talle.name for pt in talles_con_stock]
        except:
            return []
    
    def get_colores_disponibles(self, obj):
        """Obtiene colores que tienen stock > 0"""
        try:
            colores_con_stock = ProductoColor.objects.filter(
                producto=obj, 
                stock__gt=0
            ).select_related('color')
            return [pc.color.name for pc in colores_con_stock]
        except:
            return []

    def get_etiqueta(self, obj):
        """Devuelve la etiqueta del producto"""
        return obj.calcular_etiqueta()