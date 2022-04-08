from django.db import models
from django.db.models.deletion import CASCADE
from empleado.models import Empleado

class CodigoEvento(models.Model):
    cod_evento = models.CharField(max_length=10, verbose_name='Codigo de evento')
    descripcion_evento = models.CharField(max_length=500, verbose_name='Descripcion de evento')
    #Este modelo sirve para el manejo de los codigos de los eventos que 
    # comprenden dentro de los que gestiona comunmente la entidad
    class Meta: 
        db_table = 'codigo_evento'
    def __str__(self) -> str:
        return f'{self.cod_evento}'

class Evento(models.Model):
    codigo_evento = models.ForeignKey(CodigoEvento, blank=True, null=True, on_delete=CASCADE, verbose_name='Codigo del evento')
    empleado = models.ForeignKey(Empleado, blank=True, null=True, on_delete=CASCADE, verbose_name='Empleado')
    justificacion = models.CharField(max_length=500, blank=True, null=True, verbose_name='Justificacion')
    autorizado_por = models.CharField(max_length=100, blank=True, null=True, verbose_name='Autorizado por')
    fecha_inicio = models.DateField(blank=True, null=True, verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de finalizacion')
    fecha_registro = models.DateField(blank=True, null=True, verbose_name='Fecha de registro')
    usuario_registro = models.CharField(max_length=50, blank=True, null=True, verbose_name='Usuario que registró')
    # Este modelo se utiliza para registrar los eventos futuros en los cuales se justificaran las inacistencias
    # si un empleado tiene alguna situacion por la cual no asistio a trabajar debers estar registrada en este tabla
    # de lo contrario aparecera registrado en la tabla de ausencias
    class Meta:
        db_table = 'evento'    

# Create your models here.
