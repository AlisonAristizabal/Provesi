from django.contrib import admin
from .models import Bodega, Ubicacion, Producto, Inventario, MovimientoInventario, EventoOutbox
admin.site.register([Bodega, Ubicacion, Producto, Inventario, MovimientoInventario, EventoOutbox])
