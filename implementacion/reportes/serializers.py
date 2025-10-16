# reportes/serializers.py
from rest_framework import serializers
from pedidos.models import Pedido

class ResumenUbicacionSerializer(serializers.Serializer):
    ubicacion_id = serializers.IntegerField()
    ubicacion_codigo = serializers.CharField()
    pedidos_pendientes = serializers.IntegerField()


class PedidoSerializer(serializers.ModelSerializer):
    ubicacion_id = serializers.IntegerField(source="ubicacion.id", read_only=True)
    ubicacion_codigo = serializers.CharField(source="ubicacion.codigo", read_only=True)

    class Meta:
        model = Pedido
        fields = ["id", "ubicacion_id", "ubicacion_codigo", "estado", "creado_en", "actualizado_en"]
        read_only_fields = ["id", "ubicacion_id", "ubicacion_codigo", "creado_en", "actualizado_en"]

