from django.db import models
from django.core.exceptions import ValidationError


class Moneda(models.Model):
    codigo = models.CharField(max_length=3)  # Ejemplo: USD, EUR
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3)  # Código ISO de 3 letras, ej. 'USA' para Estados Unidos

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.pais.nombre}"


class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.provincia.nombre}"


class Fondo(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)

    def modificar_fondos(self, monto):
        """Aumenta o disminuye los fondos. Si el monto es negativo, reduce los fondos."""
        self.cantidad += monto
        self.save()

    def __str__(self):
        return f"{self.cantidad} {self.moneda.codigo} en {self.municipio.nombre}"


class TasaCambio(models.Model):
    moneda_base = models.ForeignKey(Moneda, related_name='moneda_base', on_delete=models.CASCADE)
    moneda_objetivo = models.ForeignKey(Moneda, related_name='moneda_objetivo', on_delete=models.CASCADE)
    tasa_normal = models.DecimalField(max_digits=10, decimal_places=4)
    tasa_real = models.DecimalField(max_digits=10, decimal_places=4)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.moneda_base.codigo} a {self.moneda_objetivo.codigo} - {self.tasa_normal}"


class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_identificacion = models.CharField(max_length=50, unique=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Mensajero(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ci = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class Transaccion(models.Model):
    remitente = models.ForeignKey(Persona, related_name='transacciones_enviadas', on_delete=models.CASCADE)
    receptor = models.ForeignKey(Persona, related_name='transacciones_recibidas', on_delete=models.CASCADE)
    cantidad_enviada = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_recibida = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mensajero = models.ForeignKey(Mensajero,related_name='mensajero', on_delete=models.CASCADE)
    costo_domicilio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    moneda_enviada = models.ForeignKey(Moneda, related_name='moneda_enviada', on_delete=models.CASCADE)
    moneda_recibida = models.ForeignKey(Moneda, related_name='moneda_recibida', on_delete=models.CASCADE)
    moneda_domicilio = models.ForeignKey(Moneda, related_name='moneda_domicilio', on_delete=models.CASCADE)
    tasa_cambio = models.ForeignKey(TasaCambio, on_delete=models.CASCADE)
    ganancia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    estados_transaccion = (
        ('Pendiente', 'Pendiente'),#de pago y de entrega
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada')
    )
    estado = models.CharField(max_length=20, choices=estados_transaccion, default='Pendiente')

    def save(self, *args, **kwargs):
        # Validar moneda y tasa de cambio
        if self.tasa_cambio.moneda_base != self.moneda_enviada or \
                self.tasa_cambio.moneda_objetivo != self.moneda_recibida:
            raise ValidationError("La tasa de cambio no coincide con las monedas enviadas y recibidas.")

        # Calcular la cantidad recibida
        self.cantidad_recibida = round(self.cantidad_enviada * self.tasa_cambio.tasa_normal, 2)

        # Calcular la cantidad real recibida
        cantidad_recibida_real = round(self.cantidad_enviada * self.tasa_cambio.tasa_real, 2)

        # Validar si hay fondos suficientes
        fondos_disponibles_receptor = Fondo.objects.filter(municipio=self.receptor.municipio,
                                                           moneda=self.moneda_recibida).first()
        fondos_disponibles_reimitente = Fondo.objects.filter(municipio=self.remitente.municipio,
                                                             moneda=self.moneda_enviada).first()

        if not fondos_disponibles_receptor:
            raise ValidationError("No hay fondos disponibles para la moneda recibida.")
        elif not fondos_disponibles_reimitente:
            raise ValidationError("No hay fondos disponibles para la moneda enviada.")

        if fondos_disponibles_receptor.cantidad < self.cantidad_recibida:
            self.ganancia = cantidad_recibida_real - self.cantidad_recibida - self.costo_domicilio
            fondos_disponibles_receptor.modificar_fondos(self.ganancia)
            fondos_disponibles_reimitente.modificar_fondos(-self.cantidad_enviada)
        else:
            self.ganancia = cantidad_recibida_real - self.cantidad_recibida - self.costo_domicilio
            fondos_disponibles_receptor.modificar_fondos(-1 * (self.cantidad_recibida + self.costo_domicilio))
            fondos_disponibles_reimitente.modificar_fondos(self.cantidad_enviada)

        super(Transaccion, self).save(*args, **kwargs)

    def __str__(self):
        return f"Transacción de {self.remitente.nombre} {self.remitente.apellido} a {self.receptor.nombre} " \
               f"{self.receptor.apellido}"
