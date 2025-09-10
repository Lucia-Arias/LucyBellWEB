from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Material, Product, Talle, Color, ProductoTalle, ProductoColor


# -----------------------------
# Inlines para Productos
# -----------------------------
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
    list_display = ['name', 'category', 'material', 'price', 'sale_price', 'total_stock', 'image_preview']
    list_filter = ['category', 'material']
    search_fields = ['name', 'description']
    readonly_fields = ['total_stock_display', 'image_preview_large']

    fieldsets = [
        ('Información Básica', {
            'fields': ['name', 'category', 'material', 'description']
        }),
        ('Precios y Stock', {
            'fields': ['price', 'price_cost', 'sale_price']
        }),
        ('Imágenes', {
            'fields': ['image', 'image_preview_large']
        }),
    ]

    inlines = [ProductoTalleInline, ProductoColorInline]


    # -----------------------------
    # Métodos para imagen
    # -----------------------------
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:30px; max-width:30px;" />', obj.image)
        return "Sin imagen"
    image_preview.short_description = 'Imagen'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px; max-width:200px;" />', obj.image)
        return "Sin imagen"
    image_preview_large.short_description = 'Vista previa'

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
# Registro de modelos
# -----------------------------
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Talle, TalleAdmin)
admin.site.register(Color, ColorAdmin)

# Personalización del admin
admin.site.site_header = 'Administración de LucyBell'
admin.site.site_title = 'LucyBell Admin'
admin.site.index_title = 'Panel de Administración'
