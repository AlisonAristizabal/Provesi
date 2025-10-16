# bodegaje/servicios.py
from django.db import transaction
from django.db.models import F
from .models import Inventario, MovimientoInventario, EventoOutbox

@transaction.atomic
def retirar_producto(*, usuario, producto, ubicacion, lote, cantidad, motivo="retiro"):
    """
    Descuenta stock de forma atómica, registra el movimiento y deja un evento en outbox.
    """
    actor = usuario if getattr(usuario, "is_authenticated", False) else None

    inv = (Inventario.objects
           .select_for_update()
           .get(producto=producto, ubicacion=ubicacion, lote=lote))
    if inv.cantidad_disponible < cantidad:
        raise ValueError("Stock insuficiente")

    inv.cantidad_disponible = F('cantidad_disponible') - cantidad
    inv.save(update_fields=['cantidad_disponible'])

    mov = MovimientoInventario.objects.create(
        tipo=MovimientoInventario.RETIRO,
        producto=producto,
        ubicacion=ubicacion,
        lote=lote,
        cantidad=cantidad,
        motivo=motivo,
        actor=actor,       # <— puede ser None
    )

    EventoOutbox.objects.create(
        tema="InventarioRetirado",
        clave=f"{producto.sku}:{ubicacion.id}:{lote}",
        carga={"sku": producto.sku, "ubicacion_id": ubicacion.id, "lote": lote,
               "cantidad": cantidad, "movimiento_id": mov.id}
    )

    # (Opcional) empujar a WebSocket de inmediato si tienes Channels configurado.
    _push_ws_sin_bloquear({
        "sku": producto.sku, "ubicacion_id": ubicacion.id, "lote": lote,
        "cantidad": cantidad, "movimiento_id": mov.id
    })
    return mov


def _push_ws_sin_bloquear(payload: dict):
    """
    Intenta enviar por WebSocket, pero no falla si Channels no está activo.
    Útil mientras montas Celery/Channels.
    """
    try:
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        capa = get_channel_layer()
        if capa:
            async_to_sync(capa.group_send)(
                "inventario_actualizaciones",
                {"type": "evento.inventario", "carga": payload}
            )
    except Exception:
        # En dev podemos ignorar silenciosamente; en prod loguea el error.
        pass
