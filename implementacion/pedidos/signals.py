# pedidos/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from reportes.views import CACHE_KEY_ESTADOS  # o define en un módulo shared, p.ej. reportes/cache_keys.py
from pedidos.models import Pedido

@receiver(post_save, sender=Pedido)
def invalidate_reportes_cache(sender, instance, **kwargs):
    cache.delete(CACHE_KEY_ESTADOS)

