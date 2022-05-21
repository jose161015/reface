from django.db import models
from django.db.models.deletion import CASCADE
from empleado.models import Empleado
from horarios.models import Horario

# Create your models here.
class Ausencias(models.Model):
    empleado = models.ForeignKey(Empleado,on_delete=CASCADE,verbose_name='Empleado')
    horario = models.ForeignKey(Horario,on_delete=CASCADE, verbose_name='Horario')
    rango_hora = models.CharField(max_length=30, blank=True, null=True,verbose_name='Rango de hora que se ausentó')
    fecha = models.DateField(blank=True, null=True, verbose_name='Fecha de ausencia')
    esta_faltando=models.BooleanField( default=True)
    justificacion_ausencia = models.CharField(max_length=500, blank=True, null=True,verbose_name='Justificación')
    fecha_modificacion=models.DateField(verbose_name='Fecha que se modificó',blank=True, null=True)
    usuario_modfico=models.CharField(max_length=50,verbose_name='Usuario que modificó',blank=True, null=True)
    # en este modelo se registraran por medio de un procedimiento en segundo plano a una hora determinada todo el
    # empleado que no haya realizado la marcacion y que no tenga un evento que justifique su ausencia  
    # se podra cambiar el estado de ausencia mediante una modificacion en administracion escribiendo los motivo 
    class Meta:
        db_table = 'ausencias'

class Marcacion(models.Model):
    empleado = models.ForeignKey(Empleado,on_delete=CASCADE,verbose_name='Empleado')
    horario = models.ForeignKey(Horario,on_delete=CASCADE,verbose_name='Horario')
    rango_horario = models.CharField(max_length=30,verbose_name='Rango horas')
    fecha_marcacion = models.DateField(verbose_name='Fecha marcacion')
    hora_entrada = models.TimeField(verbose_name='Hora entrada',blank=True, null=True)
    minutos_entrada_mas = models.CharField(verbose_name='Minutos entrada temporana',blank=True, null=True,max_length=10)
    minutos_entrada_menos = models.CharField(verbose_name='Minutos entrada tardia',blank=True, null=True,max_length=10)
    hora_salida = models.TimeField(verbose_name='Hora salida',blank=True, null=True)
    minutos_salida_mas = models.CharField(verbose_name='Minutos salida posterior',blank=True, null=True, max_length=10)
    minutos_salida_menos = models.CharField(verbose_name='Minutos salida temprana',blank=True, null=True,max_length=10)
    entrada_tardia = models.BooleanField(default= False,verbose_name='Entrada tardia')
    salida_temprana = models.BooleanField(default= False, verbose_name='Salida temprana')
    fecha_just_entrada = models.DateField(blank=True, null=True, verbose_name='Fecha justificacion')
    usuario_just_e = models.CharField(max_length=50,blank=True, null=True, verbose_name='Usuario modifico')
    justifi_entrada = models.CharField(max_length=250, blank=True, null=True, verbose_name='Comentario')
    fecha_just_salida = models.DateField(blank=True, null=True, verbose_name='Fecha justificacion')
    usuario_just_s = models.CharField(max_length=50,blank=True, null=True, verbose_name='Usuario modifico')
    justifi_salida = models.CharField(max_length=250, blank=True, null=True, verbose_name='Comentario')
    # modelo marcacion se utiliza para registrar una entrada y salida en el mismo registro conforme al horario asignado
    # al empleado 
    class Meta:
        db_table = 'marcacion'

class Urlcamaraip(models.Model):
    unidad_control=models.CharField(max_length=100,verbose_name='Unidad de Control')
    url_camara_ip=models.CharField(max_length=150,verbose_name='Url de conexión camara ip')
    es_interna=models.BooleanField( default=False, verbose_name='Marcar si es camara interna')
    class Meta:
        db_table = 'urlcamaraip'
        