from rest_framework import serializers
from .models import Transaccion, Fondo, Municipio, Moneda, Persona, Mensajero

class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = ['nombre']
        
class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['nombre']

class PersonaSerializer(serializers.ModelSerializer):
    municipio = MunicipioSerializer(read_only=True)
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'numero_identificacion', 'municipio', 'direccion', 'telefono']

class MensajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensajero
        fields = ['nombre', 'apellido', 'ci']

       
class TransaccionSerializer(serializers.ModelSerializer):
    mensajero = MensajeroSerializer(read_only=True)
    moneda_enviada = MonedaSerializer(read_only=True)
    moneda_recibida = MonedaSerializer(read_only=True)
    moneda_domicilio = MonedaSerializer(read_only=True)
    receptor = PersonaSerializer(read_only=True)
    municipio = PersonaSerializer(read_only=True)
    class Meta:
        model = Transaccion
        fields = '__all__'


class FondoSerializer(serializers.ModelSerializer):
    municipio = MunicipioSerializer(read_only=True)

    class Meta:
        model = Fondo
        fields = '__all__'


class SimpleMunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['id', 'nombre']
