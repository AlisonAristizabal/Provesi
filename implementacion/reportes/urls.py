# reportes/urls.py
from django.urls import path
from .views import ResumenUbicacionesView, PedidosPendientesView

urlpatterns = [
    path("resumen-ubicaciones/", ResumenUbicacionesView.as_view()),
    path("pedidos-pendientes/", PedidosPendientesView.as_view()),
]

