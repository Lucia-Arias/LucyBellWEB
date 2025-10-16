# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import Category, Material, Product, ProductImage
from .serializers import (
    CategorySerializer,
    MaterialSerializer,
    ProductSerializer,
    ProductListSerializer
)

# ViewSet para productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    
    def get_queryset(self):
        """Optimizar queries prefetching imágenes relacionadas"""
        queryset = Product.objects.all()
        
        # Prefetch imágenes para optimizar consultas
        if self.action in ['list', 'retrieve', 'by_category', 'on_sale', 'new_arrivals']:
            queryset = queryset.prefetch_related(
                Prefetch('images', queryset=ProductImage.objects.order_by('order', 'id'))
            )
        
        return queryset
    
    def get_serializer_class(self):
        # Usar ProductSerializer para todas las acciones para incluir todas las imágenes
        # Si necesitas un serializer más ligero para listas grandes, ajusta ProductListSerializer
        return ProductSerializer

    @action(detail=False)
    def by_category(self, request):
        category = self.request.query_params.get('category', None)
        if category:
            products = Product.objects.filter(category=category).prefetch_related(
                Prefetch('images', queryset=ProductImage.objects.order_by('order', 'id'))
            )
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Productos que tienen precio promocional"""
        products = Product.objects.filter(
            sale_price__isnull=False
        ).prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order', 'id'))
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        """Productos nuevos (últimos 7 días)"""
        from django.utils import timezone
        from datetime import timedelta
        
        one_week_ago = timezone.now() - timedelta(days=7)
        products = Product.objects.filter(
            fecha_creacion__gte=one_week_ago
        ).prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order', 'id'))
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

# ViewSet para categorías
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = category.products.all().prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order', 'id'))
        )
        serializer = ProductSerializer(products, many=True)  # Usar ProductSerializer aquí también
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
        products = material.get_products.all().prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order', 'id'))
        )
        serializer = ProductSerializer(products, many=True)  # Usar ProductSerializer aquí también
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def used_in_products(self, request):
        """Materiales que están siendo usados en productos"""
        materials = Material.objects.filter(get_products__isnull=False).distinct()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)