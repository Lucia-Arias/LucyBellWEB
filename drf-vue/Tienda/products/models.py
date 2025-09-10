from django.db import models
from django.urls import reverse

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

# Modelos de Variante (Atributo)
class VariantAttribute(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    values = models.TextField(help_text='Valores separados por coma (ej: Rojo,Azul,Verde)', verbose_name='Valores')

    class Meta:
        verbose_name = 'Atributo de Variante'
        verbose_name_plural = 'Atributos de Variantes'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_values_list(self):
        return [value.strip() for value in self.values.split(',')]
    
    def get_absolute_url(self):
        return reverse('admin:products_variantattribute_change', args=[self.id])

# Modelos de Productos
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    image = models.ImageField(upload_to='products', default='Collar Stich.png', verbose_name='Imagen')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoría')
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Precio Costo')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Precio Promocional')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='get_products', verbose_name='Material')
    has_variants = models.BooleanField(default=False, verbose_name='¿Tiene variantes?')
    variant_attributes = models.ManyToManyField(VariantAttribute, blank=True, verbose_name='Atributos de Variante')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        if self.has_variants:
            return sum(variant.stock for variant in self.variants.all())
        return 0
    
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
        # Asegurar que el nombre del archivo de imagen no tenga espacios
        if self.image and hasattr(self.image, 'name'):
            self.image.name = self.image.name.replace(' ', '_')
        super().save(*args, **kwargs)

# Modelo para variantes específicas
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Producto')
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    attributes = models.JSONField(verbose_name='Atributos')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Precio Específico')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    image = models.ImageField(upload_to='variants', null=True, blank=True, verbose_name='Imagen de Variante')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Variante de Producto'
        verbose_name_plural = 'Variantes de Producto'
        unique_together = ['product', 'attributes']
        ordering = ['sku']

    def __str__(self):
        return f"{self.product.name} - {self.get_attributes_display()}"

    def get_attributes_display(self):
        return ", ".join([f"{key}: {value}" for key, value in self.attributes.items()])

    def get_price(self):
        return self.price if self.price else self.product.price
    
    @property
    def current_price(self):
        return self.get_price()
    
    @property
    def is_on_sale(self):
        return self.product.sale_price is not None
    
    def get_absolute_url(self):
        return reverse('admin:products_productvariant_change', args=[self.id])
    
    def save(self, *args, **kwargs):
        # Generar SKU automáticamente si no se proporciona
        if not self.sku:
            base_sku = self.product.name.replace(' ', '_').upper()[:20]
            attributes_str = "_".join([f"{k[:2]}{v[:2]}" for k, v in self.attributes.items()])
            self.sku = f"{base_sku}_{attributes_str}"
        
        # Asegurar que el nombre del archivo de imagen no tenga espacios
        if self.image and hasattr(self.image, 'name'):
            self.image.name = self.image.name.replace(' ', '_')
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada si existe
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)