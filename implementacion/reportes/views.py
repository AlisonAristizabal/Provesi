# reportes/views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from django.db.models import Count, Q
from django.core.cache import cache
from django.conf import settings

from bodegaje.models import Ubicacion
from pedidos.models import Pedido
from .serializers import PedidoSerializer  # asegúrate de tenerlo (ver abajo)

# --- Estados (ajústalos a tus valores reales) ---
ESTADOS_ENVIADOS = {
    "Despachado", "Despachado x Facturar", "Entregado", "Anulado"
}
ESTADOS_NO_ENVIADOS = [
    "Alistamiento", "Por Verificar", "Rechazado x Verificar", "Verificado",
    "Empacado x Despacho", "Produccion", "Bordado", "Dropshipping",
    "Compra", "Transito",
]

# Cache
CACHE_KEY = "reportes:resumen_ubicaciones:v1"
CACHE_TTL = getattr(settings, "CACHE_TTL", settings.CACHES["default"].get("TIMEOUT", 10))


class ResumenUbicacionesView(APIView):
    """
    Devuelve una lista de ubicaciones con la cantidad de pedidos NO enviados.
    Resultado: [{"ubicacion_id": ..., "ubicacion_codigo": ..., "pedidos_pendientes": ...}, ...]
    """
    permission_classes = [AllowAny]

    def _build_payload(self):
        qs = (
            Ubicacion.objects
            .annotate(
                pendientes=Count(
                    "pedidos",
                    filter=~Q(pedidos__estado__in=ESTADOS_ENVIADOS)
                )
            )
            .filter(pendientes__gt=0)
            .values("id", "codigo", "pendientes")
            .order_by("-pendientes")
        )
        return [
            {
                "ubicacion_id": r["id"],
                "ubicacion_codigo": r["codigo"],
                "pedidos_pendientes": r["pendientes"],
            }
            for r in qs
        ]

    def get(self, request):
        data = cache.get(CACHE_KEY)
        if data is None:
            data = self._build_payload()
            cache.set(CACHE_KEY, data, timeout=CACHE_TTL)
        return Response(data)


class PedidosPendientesView(ListAPIView):
    """
    Lista de pedidos NO enviados con info de ubicación.
    """
    permission_classes = [AllowAny]
    serializer_class = PedidoSerializer
    pagination_class = None  # o usa la paginación global si la tienes

    def get_queryset(self):
        return (
            Pedido.objects
            .select_related("ubicacion")
            .filter(estado__in=ESTADOS_NO_ENVIADOS)
            .order_by("-creado_en")
        )
