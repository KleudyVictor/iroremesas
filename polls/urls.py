from django.urls import path
from .views import TransaccionRangoFechaView, TransaccionPorMunicipioView, FondoPorMunicipioView, \
    ResumenTransaccionesView, MunicipioListView, FondoTotalesView, TransaccionesPendientesView

urlpatterns = [
    path('transacciones/rango/<fecha_inicio>/<fecha_fin>/', TransaccionRangoFechaView.as_view()),
    path('transacciones/municipio/<int:municipio_id>/<fecha_inicio>/<fecha_fin>/', 
         TransaccionPorMunicipioView.as_view()),
    path('fondos/municipio/<int:municipio_id>/', FondoPorMunicipioView.as_view()),
    path('fondostotales/', FondoTotalesView.as_view()),
    path('resumen/transacciones/', ResumenTransaccionesView.as_view()),
    path('municipios/', MunicipioListView.as_view()),
    path('pendientes/<str:ci>/', TransaccionesPendientesView.as_view()),
]
