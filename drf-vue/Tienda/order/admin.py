from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "cliente_nombre", "metodo_envio", "metodo_pago", "creado_en", "completado"]
    list_filter = ["metodo_envio", "metodo_pago", "completado"]
    search_fields = ["cliente_nombre", "cliente_telefono"]
