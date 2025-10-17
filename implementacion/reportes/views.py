# reportes/views.py
from django.db.models import Count, Q
from django.core.cache import cache
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from pedidos.models import Pedido
from .serializers import ResumenEstadoSerializer, PedidoSerializer

ESTADOS_ENVIADOS = {"Despachado", "Despachado x Facturar", "Entregado", "Anulado"}
CACHE_KEY_ESTADOS = "reportes:resumen_estados:v1"

class ResumenEstadosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = cache.get(CACHE_KEY_ESTADOS)
        if data is None:
            qs = (
                Pedido.objects
                .values("estado")
                .annotate(pedidos_pendientes=Count("id", filter=~Q(estado__in=ESTADOS_ENVIADOS)))
                .filter(pedidos_pendientes__gt=0)
                .order_by("-pedidos_pendientes")
            )
            data = list(qs)  # [{'estado': 'Alistamiento', 'pedidos_pendientes': 120}, ...]
            cache.set(CACHE_KEY_ESTADOS, data, timeout=settings.CACHES["default"].get("TIMEOUT", 10))

        # (opcional) validar con serializer
        return Response(ResumenEstadoSerializer(data, many=True).data)


# (opcional) listar pedidos por un estado puntual (solo pendientes)
class PedidosPendientesPorEstadoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, estado):
        if estado in ESTADOS_ENVIADOS:
            return Response([])  # no listamos enviados aquí
        qs = (Pedido.objects
              .select_related("ubicacion")
              .filter(estado=estado)
              .order_by("-creado_en"))
        return Response(PedidoSerializer(qs, many=True).data)
