from django.db import models
from django.utils import timezone
from cart.models import Cart

class Order(models.Model):
    METODOS_ENVIO = [
        ('olmos', 'Retiro en Patio Olmos (Miércoles 17:15 hs)'),
        ('cadete', 'Envío por cadete Uber (pago previo)'),
        ('domicilio', 'Retiro por mi domicilio (horario a coordinar)'),
        ('plaza', 'Plaza Rivadavia (fines de semana 16 a 20 hs)'),
    ]

    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ]

    OPCIONES_ENTREGA = [
        ('ahora', 'Lo antes posible'),
        ('hoy', 'Hoy a tal hora'),
        ('mañana', 'Mañana a tal hora'),
        ('fecha', 'En una fecha específica'),
    ]

    cliente_nombre = models.CharField(max_length=255, verbose_name="Nombre del cliente")
    cliente_telefono = models.CharField(max_length=20, verbose_name="Teléfono de contacto", null=True, blank=True)

    metodo_envio = models.CharField(max_length=20, choices=METODOS_ENVIO)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)

    # Solo si elige envío
    opcion_entrega = models.CharField(max_length=20, choices=OPCIONES_ENTREGA, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    carrito = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="pedido")

    creado_en = models.DateTimeField(default=timezone.now)
    completado = models.BooleanField(default=False)

    def total(self):
        return self.carrito.total()

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"
