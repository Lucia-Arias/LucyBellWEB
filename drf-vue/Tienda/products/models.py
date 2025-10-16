from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


# Modelos de Color
class Color(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('admin:products_color_change', args=[self.id])
    
    
# Modelos de Talle
class Talle(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Talle'
        verbose_name_plural = 'Talles'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('admin:products_talle_change', args=[self.id])

# Modelos de Categoria
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('admin:products_category_change', args=[self.id])

# Modelos de Material
class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('admin:products_material_change', args=[self.id])


# Modelo para las imágenes del producto
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', verbose_name='Producto')
    image = models.URLField(max_length=255, verbose_name='URL de la imagen')
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name='Texto alternativo')
    
    class Meta:
        verbose_name = 'Imagen del producto'
        verbose_name_plural = 'Imágenes del producto'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"Imagen de {self.product.name}"


# Modelos de Productos
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    # Removemos el campo image del modelo principal
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoría')
    description = models.TextField(verbose_name='Descripción', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Precio Costo')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Precio Promocional')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='get_products', verbose_name='Material')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='get_products', verbose_name='Color')
    talle = models.ForeignKey(Talle, on_delete=models.SET_NULL, null=True, blank=True, related_name='get_products', verbose_name='Talle')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    @property
    def main_image(self):
        """Devuelve la imagen principal (primera imagen ordenada)"""
        first_image = self.images.first()
        return first_image.image if first_image else None
    
    @property
    def image_list(self):
        """Devuelve lista de todas las URLs de imágenes"""
        return [img.image for img in self.images.all()]
    
    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price
    
    @property
    def profit_margin(self):
        if self.price_cost and self.price:
            return ((self.price - self.price_cost) / self.price_cost) * 100
        return 0
    
    def get_absolute_url(self):
        return reverse('admin:products_product_change', args=[self.id])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def calcular_etiqueta(self):
        # Obtener el stock total de todos los talles
        total_stock = sum(pt.stock for pt in self.productotalle_set.all())

        if total_stock == 1:
            return "Última unidad"
        elif self.sale_price and self.sale_price < self.price:
            return "Descuento"
        elif timezone.now() - self.fecha_creacion <= timedelta(days=7):
            return "Nuevo ingreso"
        return None


class ProductoTalle(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    talle = models.ForeignKey(Talle, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = 'producto_talle'
        unique_together = ('producto', 'talle')

@receiver(post_save, sender=ProductoTalle)
def actualizar_etiqueta_producto(sender, instance, **kwargs):
    producto = instance.producto
    producto.save()  # Esto volverá a calcular la etiqueta

class ProductoColor(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = 'producto_color'
        unique_together = ('producto', 'color')