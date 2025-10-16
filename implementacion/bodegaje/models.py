from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Bodega(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    direccion = models.CharField(max_length=180)
    def __str__(self): return self.codigo

class Ubicacion(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='ubicaciones')
    codigo = models.CharField(max_length=30)
    nombre = models.CharField(max_length=80, blank=True, default="")
    class Meta: unique_together = (('bodega','codigo'),)
    def __str__(self): return f"{self.bodega.codigo}-{self.codigo}"

class Producto(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=120)
    def __str__(self): return f"{self.sku} - {self.nombre}"

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    lote = models.CharField(max_length=40, blank=True)
    cantidad_disponible = models.IntegerField()
    cantidad_reservada = models.IntegerField(default=0)
    class Meta:
        unique_together = (('producto','ubicacion','lote'),)
        indexes = [models.Index(fields=['ubicacion']),
                   models.Index(fields=['producto','lote'])]

class MovimientoInventario(models.Model):
    RETIRO, AJUSTE = 'RETIRO', 'AJUSTE'
    tipo = models.CharField(max_length=20, choices=[(RETIRO,'Retiro'),(AJUSTE,'Ajuste')], default=RETIRO)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    lote = models.CharField(max_length=40, blank=True)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=160)
    actor = models.ForeignKey(get_user_model(),
        null=True, blank=True,                # <— permite anónimo
        on_delete=models.SET_NULL,
        related_name="movimientos")
    creado_en = models.DateTimeField(auto_now_add=True)

class EventoOutbox(models.Model):
    tema = models.CharField(max_length=80)
    clave = models.CharField(max_length=120)
    carga = models.JSONField()
    creado_en = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=False)
