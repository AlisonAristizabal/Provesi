# reportes/serializers.py
from rest_framework import serializers
from pedidos.models import Pedido

class ResumenEstadoSerializer(serializers.Serializer):
    estado = serializers.CharField()
    pedidos_pendientes = serializers.IntegerField()

# (Si ya tienes PedidoSerializer, déjalo como está)
class PedidoSerializer(serializers.ModelSerializer):
    ubicacion_id = serializers.IntegerField(source="ubicacion.id", read_only=True)
    ubicacion_codigo = serializers.CharField(source="ubicacion.codigo", read_only=True)

    class Meta:
        model = Pedido
        fields = ["id", "ubicacion_id", "ubicacion_codigo", "estado", "creado_en", "actualizado_en"]
