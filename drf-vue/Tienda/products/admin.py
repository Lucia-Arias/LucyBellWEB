from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Material, Product, Talle, Color, ProductoTalle, ProductoColor, ProductImage


# -----------------------------
# Inlines para Productos
# -----------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'order', 'alt_text', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px; max-width:50px;" />', obj.image)
        return "Sin imagen"
    image_preview.short_description = 'Vista previa'


class ProductoTalleInline(admin.TabularInline):
    model = ProductoTalle
    extra = 1
    autocomplete_fields = ['talle']


class ProductoColorInline(admin.TabularInline):
    model = ProductoColor
    extra = 1
    autocomplete_fields = ['color']


# -----------------------------
# Admin para Product
# -----------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'material', 'price', 'sale_price', 'total_stock', 'main_image_preview']
    list_filter = ['category', 'material']
    search_fields = ['name', 'description']
    readonly_fields = ['total_stock_display', 'main_image_preview_large', 'profit_margin_display', 'fecha_creacion_display']
    
    fieldsets = [
        ('Información Básica', {
            'fields': ['name', 'category', 'material', 'color', 'talle', 'description']
        }),
        ('Precios', {
            'fields': ['price', 'price_cost', 'sale_price', 'profit_margin_display']
        }),
        ('Imagen Principal', {
            'fields': ['main_image_preview_large']
        }),
        ('Stock y Fechas', {
            'fields': ['total_stock_display', 'fecha_creacion_display']
        }),
    ]

    inlines = [ProductImageInline, ProductoTalleInline, ProductoColorInline]

    # -----------------------------
    # Métodos para imagen principal
    # -----------------------------
    def main_image_preview(self, obj):
        """Vista previa pequeña para la lista de productos"""
        main_image = obj.main_image
        if main_image:
            return format_html('<img src="{}" style="max-height:50px; max-width:50px;" />', main_image)
        return "Sin imagen"
    main_image_preview.short_description = 'Imagen Principal'

    def main_image_preview_large(self, obj):
        """Vista previa grande para el formulario de edición"""
        main_image = obj.main_image
        if main_image:
            return format_html('<img src="{}" style="max-height:200px; max-width:200px;" />', main_image)
        return "No hay imagen principal"
    main_image_preview_large.short_description = 'Vista previa de imagen principal'

    # -----------------------------
    # Stock total (talles + colores)
    # -----------------------------
    def total_stock(self, obj):
        stock_talles = sum(pt.stock for pt in obj.productotalle_set.all())
        stock_colores = sum(pc.stock for pc in obj.productocolor_set.all())
        return stock_talles + stock_colores
    total_stock.short_description = 'Stock Total'

    def total_stock_display(self, obj):
        return self.total_stock(obj)
    total_stock_display.short_description = 'Stock Total'

    # -----------------------------
    # Margen de ganancia
    # -----------------------------
    def profit_margin_display(self, obj):
        return f"{obj.profit_margin:.2f}%"
    profit_margin_display.short_description = 'Margen de Ganancia'

    # -----------------------------
    # Fecha de creación
    # -----------------------------
    def fecha_creacion_display(self, obj):
        return obj.fecha_creacion.strftime("%d/%m/%Y %H:%M")
    fecha_creacion_display.short_description = 'Fecha de Creación'


# -----------------------------
# Admin para Category
# -----------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Número de Productos'


# -----------------------------
# Admin para Material
# -----------------------------
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']
    search_fields = ['name']

    def product_count(self, obj):
        return obj.get_products.count()
    product_count.short_description = 'Número de Productos'


# -----------------------------
# Admin para Talle
# -----------------------------
class TalleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# -----------------------------
# Admin para Color
# -----------------------------
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# -----------------------------
# Admin para ProductImage
# -----------------------------
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'order', 'alt_text']
    list_filter = ['product']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['image_preview_large']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px; max-width:50px;" />', obj.image)
        return "Sin imagen"
    image_preview.short_description = 'Vista previa'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px; max-width:200px;" />', obj.image)
        return "Sin imagen"
    image_preview_large.short_description = 'Vista previa grande'


# -----------------------------
# Registro de modelos
# -----------------------------
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Talle, TalleAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)

# Personalización del admin
admin.site.site_header = 'Administración de LucyBell'
admin.site.site_title = 'LucyBell Admin'
admin.site.index_title = 'Panel de Administración'