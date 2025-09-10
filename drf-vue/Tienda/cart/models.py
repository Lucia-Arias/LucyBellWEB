from django.db import models
from products.models import Product, Color, Talle

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    talle = models.ForeignKey(Talle, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        # Usa sale_price si hay descuento
        price = self.product.sale_price if self.product.is_on_sale else self.product.price
        return price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # compra finalizada

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito {self.id} - {'Completado' if self.completed else 'Activo'}"
