from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaccion, Fondo, Municipio, Persona
from .serializers import TransaccionSerializer, FondoSerializer, SimpleMunicipioSerializer
from django.db.models import Sum
from django.db.models.functions import Coalesce
import datetime
from django.utils import timezone


def validar_fechas(fecha_inicio, fecha_fin):
    try:
        fecha_inicio = timezone.make_aware(datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.datetime.strptime(fecha_fin, '%Y-%m-%d'))
        if fecha_inicio > fecha_fin:
            return None, 'La fecha de inicio debe ser menor que la fecha de fin'
        return (fecha_inicio, fecha_fin), None
    except ValueError:
        return None, 'Formato de fecha incorrecto, debe ser YYYY-MM-DD'


class TransaccionRangoFechaView(APIView):

    def get(self, request, fecha_inicio, fecha_fin):
        fechas, error = validar_fechas(fecha_inicio, fecha_fin)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        transacciones = Transaccion.objects.filter(fecha_transaccion__range=fechas)
        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data)


class TransaccionPorMunicipioView(APIView):

    def get(self, request, municipio_id, fecha_inicio, fecha_fin):
        fechas, error = validar_fechas(fecha_inicio, fecha_fin)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        transacciones = Transaccion.objects.filter(receptor__municipio_id=municipio_id, fecha_transaccion__range=fechas)
        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data)


class FondoPorMunicipioView(APIView):

    def get(self, request, municipio_id):
        try:
            municipio_id = int(municipio_id)
        except ValueError:
            return Response({'error': 'ID de municipio inválido'}, status=status.HTTP_400_BAD_REQUEST)

        fondos = Fondo.objects.filter(municipio_id=municipio_id)
        serializer = FondoSerializer(fondos, many=True)
        return Response(serializer.data)

class FondoTotalesView(APIView):

    def get(self, request):

        fondos_totales = Fondo.objects.all()
        serializer = FondoSerializer(fondos_totales, many=True)
        return Response(serializer.data)
    
class ResumenTransaccionesView(APIView):

    def get(self, request):
        total_transacciones = Transaccion.objects.all().count()
        total_clientes = Persona.objects.all().count()
        cantidad_transacciones_pendientes = Transaccion.objects.filter(estado='Pendiente').count()
        total_ganancias = Transaccion.objects.aggregate(Sum('ganancia'))
        return Response({
            'total_transacciones': total_transacciones,
            'total_clientes': total_clientes,
            'cantidad_transacciones_pendientes': cantidad_transacciones_pendientes,
            'total_ganancias': total_ganancias,
        })

class MunicipioListView(APIView):
    def get(self, request):
        municipios = Municipio.objects.all()
        serializer = SimpleMunicipioSerializer(municipios, many=True)
        return Response(serializer.data)
    
class TransaccionesPendientesView(APIView): 
    def get(self, request, ci):
        transacciones_pendientes = Transaccion.objects.filter(estado='Pendiente', mensajero__ci=ci)
        serializer = TransaccionSerializer(transacciones_pendientes, many=True)
        return Response(serializer.data)