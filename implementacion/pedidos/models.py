# pedidos/models.py
from django.db import models
from bodegaje.models import Ubicacion

class Pedido(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name="pedidos")
    estado = models.CharField(max_length=50)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"

