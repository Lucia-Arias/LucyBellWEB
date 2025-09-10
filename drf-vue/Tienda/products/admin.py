from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Material, Product, VariantAttribute, ProductVariant

# Admin para VariantAttribute
class VariantAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_values_list_display', 'product_count']
    search_fields = ['name', 'values']
    list_filter = ['name']
    
    def get_values_list_display(self, obj):
        return ", ".join(obj.get_values_list()[:3]) + ("..." if len(obj.get_values_list()) > 3 else "")
    get_values_list_display.short_description = 'Valores'
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Productos'

# Admin inline para ProductVariant
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['sku', 'attributes_display', 'price', 'stock', 'image_preview']
    readonly_fields = ['attributes_display', 'image_preview']
    
    def attributes_display(self, obj):
        return obj.get_attributes_display()
    attributes_display.short_description = 'Atributos'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Sin imagen"
    image_preview.short_description = 'Vista previa'

# Admin para Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'material', 'price', 'sale_price', 'total_stock', 'has_variants', 'image_preview']
    list_filter = ['category', 'material', 'has_variants']
    search_fields = ['name', 'description']
    filter_horizontal = ['variant_attributes']
    inlines = [ProductVariantInline]
    readonly_fields = ['total_stock_display', 'image_preview_large']
    fieldsets = [
        ('Información Básica', {
            'fields': ['name', 'category', 'material', 'description']
        }),
        ('Precios y Stock', {
            'fields': ['price', 'price_cost', 'sale_price', 'total_stock_display']
        }),
        ('Imágenes', {
            'fields': ['image', 'image_preview_large']
        }),
        ('Variantes', {
            'fields': ['has_variants', 'variant_attributes']
        }),
    ]
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 30px;" />', obj.image.url)
        return "Sin imagen"
    image_preview.short_description = 'Imagen'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
        return "Sin imagen"
    image_preview_large.short_description = 'Vista previa de imagen'
    
    def total_stock_display(self, obj):
        return obj.total_stock
    total_stock_display.short_description = 'Stock Total'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Si el producto ya no tiene variantes, eliminar todas sus variantes
        if not obj.has_variants:
            obj.variants.all().delete()

# Admin para ProductVariant
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['sku', 'product', 'attributes_display', 'stock', 'price_display', 'image_preview']
    list_filter = ['product', 'product__category']
    search_fields = ['sku', 'product__name', 'attributes']
    readonly_fields = ['attributes_display', 'image_preview_large']
    fieldsets = [
        ('Información Básica', {
            'fields': ['product', 'sku']
        }),
        ('Atributos y Stock', {
            'fields': ['attributes', 'attributes_display', 'stock']
        }),
        ('Precios', {
            'fields': ['price', 'current_price_display']
        }),
        ('Imagen', {
            'fields': ['image', 'image_preview_large']
        }),
    ]
    
    def attributes_display(self, obj):
        return obj.get_attributes_display()
    attributes_display.short_description = 'Atributos (visualización)'
    
    def price_display(self, obj):
        return obj.get_price()
    price_display.short_description = 'Precio'
    
    def current_price_display(self, obj):
        return obj.get_price()
    current_price_display.short_description = 'Precio Actual'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 30px;" />', obj.image.url)
        elif obj.product.image:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 30px;" />', obj.product.image.url)
        return "Sin imagen"
    image_preview.short_description = 'Imagen'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
        elif obj.product.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.product.image.url)
        return "Sin imagen"
    image_preview_large.short_description = 'Vista previa de imagen'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtrar productos que tienen variantes habilitadas
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(has_variants=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Admin para Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Número de Productos'

# Admin para Material
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.get_products.count()
    product_count.short_description = 'Número de Productos'

# Registro de modelos
admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(VariantAttribute, VariantAttributeAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)

# Opcional: Personalizar el título del admin
admin.site.site_header = 'Administración de LucyBell'
admin.site.site_title = 'LucyBell Admin'
admin.site.index_title = 'Panel de Administración'