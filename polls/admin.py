from django.contrib import admin
from .models import Moneda, Pais, Provincia, Municipio, Fondo, TasaCambio, Persona, Transaccion, Mensajero


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    list_filter = ('nombre',)
    search_fields = ('codigo', 'nombre')


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais')
    list_filter = ('pais',)
    search_fields = ('nombre', 'pais')


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia')
    list_filter = ('provincia',)
    search_fields = ('nombre', 'provincia')


@admin.register(Fondo)
class FondoAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'moneda', 'cantidad')
    list_filter = ('municipio', 'moneda')
    search_fields = ('municipio', 'moneda')


@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = ('moneda_base', 'moneda_objetivo', 'tasa_normal', 'tasa_real', 'fecha')
    list_filter = ('moneda_base', 'moneda_objetivo', 'fecha')
    search_fields = ('moneda_base', 'moneda_objetivo', 'fecha')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'numero_identificacion', 'municipio', 'direccion', 'telefono')
    list_filter = ('municipio',)
    search_fields = ('nombre', 'apellido', 'numero_identificacion', 'municipio', 'direccion', 'telefono')
    
@admin.register(Mensajero)
class MensajeroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'ci')
    list_filter = ('nombre', 'ci')
    search_fields = ('nombre', 'apellido', 'ci')


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('estado', 'remitente', 'receptor', 'cantidad_enviada', 'cantidad_recibida', 'moneda_enviada',
                    'moneda_recibida', 'tasa_cambio', 'fecha_transaccion')
    list_filter = ('estado', 'remitente', 'receptor', 'moneda_enviada', 'moneda_recibida', 'fecha_transaccion')
    search_fields = ('remitente__nombre', 'receptor__nombre', 'moneda_enviada__codigo', 'moneda_recibida__codigo',
                     'cantidad_enviada', 'cantidad_recibida')
    # raw_id_fields = ('remitente', 'receptor', 'moneda_enviada', 'moneda_recibida', 'tasa_cambio') # Línea comentada
    date_hierarchy = 'fecha_transaccion'
    ordering = ('-fecha_transaccion',)
    readonly_fields = ('cantidad_recibida', 'ganancia')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('remitente', 'receptor', 'moneda_enviada', 'moneda_recibida', 'tasa_cambio')
        return queryset
