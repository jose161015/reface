from django.db import models
from django.db.models.deletion import CASCADE
from empleado.models import Empleado

# Create your models here.
class TipoHorario(models.Model):
    descripcion = models.CharField(max_length=30, verbose_name='Tipo de horario')
    # este modelo establece el tipo de horario de acuerdo al departamento de pertenencia 
    # se puede crear un tipo de horario especial que puede estar excluido de los periodos de vacacion y asueto
    # para que la marcacion se realice a ese grupo especial de empleados 
    class Meta:
        db_table = 'tipohorario'
    def __str__(self) -> str:
        return f'{self.descripcion}'

class Horario(models.Model):
    descripcion = models.CharField( max_length=30, verbose_name='Nombre de horario')  
    tipohorario = models.ForeignKey(TipoHorario, on_delete=CASCADE, verbose_name='Tipo de horario')
    # en este caso se ha ingresado los horarios expresados en la normativa
    # por ejemplo hemos antepuesto el prefijo de administracion acompañado de un guion y al final el numero del horario  
    # quedando de la siguiente manera admon-1
    class Meta:
        db_table = 'horario'
    def __str__(self) -> str:
        return f'{self.descripcion}'

class RangoHora(models.Model):
    rango_hora = models.CharField(max_length=15, blank=True, null=True, verbose_name='Rango de hora')
    hora_inicio = models.TimeField(blank=True, null=True, verbose_name='Hora de inicio')
    hora_fin = models.TimeField(blank=True, null=True, verbose_name='Hora de finalizacion')
    # este modelo se agrega los rangos de horas en un turno de trabajo para ser mas facil la visualizacion
    # se pide se escriba el rango de hora al que hace referencia

    class Meta:
        db_table = 'rangohora'
    def __str__(self) -> str:
        return f'{self.rango_hora}'

class Turno(models.Model):
    rango_hora = models.ForeignKey(RangoHora, blank=True, null=True,on_delete=CASCADE,verbose_name='Hora')
    dia = models.CharField(max_length=10,verbose_name='Dia')
    horario = models.ForeignKey(Horario, blank=True, null=True,on_delete=CASCADE,verbose_name='Horario')
    # En este modelo se asignan los rangos de hora los dias y el tipo de horario el cual debe de construirse 
    # para todos los horarios en los dias segun sea necesario de esta forma se puede manejar la marcacion fragmentada 
    # segun es requerido
    class Meta:
        db_table = 'turno'

class AsigHorario(models.Model):
    empleado = models.ForeignKey(Empleado,blank=True, on_delete=CASCADE, null=True,verbose_name='Id del Empleado')
    horario = models.ForeignKey(Horario,blank=True, null=True, verbose_name='Id del Horario', on_delete=CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True, verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de finalizacion')
    fecha_registro = models.DateTimeField(verbose_name='Fecha de registro')
    usuario_registro = models.CharField(max_length=50, blank=True, null=True, verbose_name='Usuario que asiga horario')
    # este modelo se utiliza para asignar un horario a un empleado si el empleado no tiene asignado horario o si este
    # ya vencio o caducó, no podra realizar la marcacion por lo que debera ir a administraciona que le extienda la vigencia 
    # o le asigen un nuevo horario
    class Meta:
        verbose_name='AsigHorario'
        verbose_name_plural='AsigHorarios'
        db_table = 'asig_horario'

class Asueto(models.Model):
   nombre_asueto=models.CharField(max_length=50, verbose_name='Escriba el nombre del Asueto')
   fecha_inicio=models.DateField(verbose_name='Fecha de inicio')
   fecha_finalizacion=models.DateField(verbose_name='fecha de finalizacion')
   tipohorario=models.ManyToManyField(TipoHorario)
   # En este modelo se asignaran los tipos de horarios que gozaran de los asueto que se registran en este modelo
   # con la modalidad de uno a muchos  
   class Meta:
        db_table = 'asueto'
        ordering=['fecha_inicio']
        
   def __str__(self) -> str:
        return f'{self.nombre_asueto}'