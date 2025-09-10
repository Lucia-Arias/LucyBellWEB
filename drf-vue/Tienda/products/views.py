from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Material, Product
from .serializers import (
    CategorySerializer,
    MaterialSerializer,
    ProductSerializer,
    ProductListSerializer
)

# ViewSet para productos
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

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Productos que tienen precio promocional"""
        products = Product.objects.filter(sale_price__isnull=False)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

# ViewSet para categorías
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

# ViewSet para materiales
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
