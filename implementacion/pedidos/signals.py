# pedidos/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from reportes.cache_keys import RESUMEN_UBICACIONES_KEY as CACHE_KEY

 # o define la key en reportes/cache_keys.py

from .models import Pedido

@receiver([post_save, post_delete], sender=Pedido)
def invalidate_resumen_cache(*args, **kwargs):
    cache.delete(CACHE_KEY)
