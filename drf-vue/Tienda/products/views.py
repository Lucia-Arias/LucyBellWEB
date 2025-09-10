from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response 
from .models import Category, Material, Product, VariantAttribute, ProductVariant
from .serializers import (
    CategorySerializer, 
    MaterialSerializer, 
    ProductSerializer, 
    VariantAttributeSerializer,
    ProductVariantSerializer,
    ProductListSerializer,
    ProductVariantCreateSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        # Usar serializer diferente para listado vs detalle/creación
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @action(detail=False)
    def by_category(self, request):
        category = self.request.query_params.get('category', None)
        if category:
            products = Product.objects.filter(category=category)
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        product = self.get_object()
        variants = product.variants.all()
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Productos que tienen precio promocional"""
        products = Product.objects.filter(sale_price__isnull=False)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def with_variants(self, request):
        """Productos que tienen variantes"""
        products = Product.objects.filter(has_variants=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = category.products.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def with_products(self, request):
        """Categorías que tienen productos"""
        categories = Category.objects.filter(products__isnull=False).distinct()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        material = self.get_object()
        products = material.get_products.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def used_in_products(self, request):
        """Materiales que están siendo usados en productos"""
        materials = Material.objects.filter(get_products__isnull=False).distinct()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

class VariantAttributeViewSet(viewsets.ModelViewSet):
    queryset = VariantAttribute.objects.all()
    serializer_class = VariantAttributeSerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        attribute = self.get_object()
        products = Product.objects.filter(variant_attributes=attribute)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def used_in_products(self, request):
        """Atributos que están siendo usados en productos"""
        attributes = VariantAttribute.objects.filter(product__isnull=False).distinct()
        serializer = VariantAttributeSerializer(attributes, many=True)
        return Response(serializer.data)

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    
    def get_serializer_class(self):
        # Usar serializer diferente para creación/actualización
        if self.action in ['create', 'update', 'partial_update']:
            return ProductVariantCreateSerializer
        return ProductVariantSerializer

    @action(detail=False)
    def by_product(self, request):
        product_id = self.request.query_params.get('product', None)
        if product_id:
            variants = ProductVariant.objects.filter(product=product_id)
            serializer = ProductVariantSerializer(variants, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False)
    def low_stock(self, request):
        threshold = int(self.request.query_params.get('threshold', 5))
        variants = ProductVariant.objects.filter(stock__lte=threshold)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def out_of_stock(self, request):
        """Variantes sin stock"""
        variants = ProductVariant.objects.filter(stock=0)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Actualizar stock de una variante específica"""
        variant = self.get_object()
        new_stock = request.data.get('stock')
        
        if new_stock is not None:
            try:
                variant.stock = int(new_stock)
                variant.save()
                serializer = ProductVariantSerializer(variant)
                return Response(serializer.data)
            except ValueError:
                return Response(
                    {'error': 'Stock debe ser un número válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {'error': 'Campo stock es requerido'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False)
    def by_attribute(self, request):
        """Variantes filtradas por atributo específico"""
        attribute_name = self.request.query_params.get('attribute')
        attribute_value = self.request.query_params.get('value')
        
        if attribute_name and attribute_value:
            # Filtrar variantes que tengan el atributo y valor específicos
            variants = ProductVariant.objects.filter(
                attributes__has_key=attribute_name,
                attributes__contains={attribute_name: attribute_value}
            )
            serializer = ProductVariantSerializer(variants, many=True)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Parámetros attribute y value son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )