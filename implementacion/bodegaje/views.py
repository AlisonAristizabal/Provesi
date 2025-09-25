from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Producto, Ubicacion
from .servicios import retirar_producto

class RetiroView(APIView):
    permission_classes = [IsAuthenticated]  # En dev puedes usar AllowAny

    def post(self, request):
        data = request.data
        producto = get_object_or_404(Producto, sku=data['sku'])
        ubicacion = get_object_or_404(Ubicacion, id=data['ubicacion_id'])
        mov = retirar_producto(
            usuario=request.user,
            producto=producto,
            ubicacion=ubicacion,
            lote=data.get('lote', ''),
            cantidad=int(data['cantidad']),
            motivo=data.get('motivo', 'retiro'),
        )
        return Response({
            "id": mov.id,
            "sku": producto.sku,
            "ubicacion_id": ubicacion.id,
            "lote": mov.lote,
            "cantidad": mov.cantidad,
            "motivo": mov.motivo,
            "creado_en": mov.creado_en,
        }, status=201)
