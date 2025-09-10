from rest_framework import serializers
from .models import Category, Material, Product, ProductVariant, VariantAttribute

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class VariantAttributeSerializer(serializers.ModelSerializer):
    values_list = serializers.SerializerMethodField()
    
    class Meta:
        model = VariantAttribute
        fields = '__all__'
    
    def get_values_list(self, obj):
        return obj.get_values_list()

class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    attributes_display = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    on_sale = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = '__all__'
        read_only_fields = ('sku',)
    
    def get_attributes_display(self, obj):
        return obj.get_attributes_display()
    
    def get_current_price(self, obj):
        return obj.get_price()
    
    def get_on_sale(self, obj):
        return obj.product.sale_price is not None

class ProductSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar información relacionada
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    
    # Campos calculados
    total_stock = serializers.IntegerField(read_only=True)
    has_variants_display = serializers.BooleanField(source='has_variants', read_only=True)
    
    # Relaciones
    variants = ProductVariantSerializer(many=True, read_only=True)
    variant_attributes_list = VariantAttributeSerializer(
        source='variant_attributes', 
        many=True, 
        read_only=True
    )
    
    # Precio promocional (si existe)
    sale_price_display = serializers.DecimalField(
        source='sale_price', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        """
        Personaliza la representación para ocultar variantes 
        si el producto no las tiene
        """
        representation = super().to_representation(instance)
        
        # Si el producto no tiene variantes, removemos el campo variants
        if not instance.has_variants:
            representation.pop('variants', None)
        
        # Si no tiene atributos de variante, removemos la lista
        if not instance.variant_attributes.exists():
            representation.pop('variant_attributes_list', None)
        
        return representation
    
    def validate(self, data):
        """
        Validación personalizada para el producto
        """
        # Validar que price_cost no sea mayor que price
        price_cost = data.get('price_cost')
        price = data.get('price')
        
        if price_cost and price and price_cost > price:
            raise serializers.ValidationError(
                "El precio de costo no puede ser mayor que el precio de venta"
            )
        
        # Validar que sale_price sea menor que price si existe
        sale_price = data.get('sale_price')
        if sale_price and price and sale_price >= price:
            raise serializers.ValidationError(
                "El precio promocional debe ser menor que el precio regular"
            )
        
        return data

# Serializer para crear/actualizar variantes con validación
class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
    
    def validate_attributes(self, value):
        """
        Validar que los atributos coincidan con los definidos en el producto
        """
        product = self.initial_data.get('product')
        if product:
            product_obj = Product.objects.get(pk=product)
            if product_obj.has_variants:
                for attr_name in value.keys():
                    if not product_obj.variant_attributes.filter(name=attr_name).exists():
                        raise serializers.ValidationError(
                            f"El atributo '{attr_name}' no está definido para este producto"
                        )
        return value

# Serializer para listado rápido de productos
class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'category', 'category_name', 
            'material', 'material_name', 'price', 'sale_price',
            'total_stock', 'has_variants'
        ]