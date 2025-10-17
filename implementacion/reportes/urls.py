# reportes/urls.py
from django.urls import path
from .views import ResumenEstadosView, PedidosPendientesPorEstadoView

urlpatterns = [
    path("resumen-estados/", ResumenEstadosView.as_view()),
    path("pendientes/<str:estado>/", PedidosPendientesPorEstadoView.as_view()),
]

