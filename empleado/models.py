from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Ocupacion(models.Model):
    nom_ocupacion = models.CharField(max_length=50, verbose_name='Ocupacion o puesto de trabajo')
    # Este modelo srive para asiganerle una ocupacion que desempeña el empleado dentro de la organizacion
    class Meta:   
        db_table = 'ocupacion'
    def __str__(self) -> str:
        return f'{self.nom_ocupacion}'

class Departamento(models.Model):
    nom_departamento = models.CharField(max_length=50, verbose_name='Departamento o unidad de pertenencia')
    #este modelo sirve para asignar un departamento de pertenencia al empleado dentro de la organizacion
    
    class Meta:   
        db_table = 'departamento'
    
    def __str__(self):
        return f'{self.nom_departamento}'


class Empleado(models.Model):
    carnet_empleado = models.CharField(max_length=11, unique=True,verbose_name='Carnet de empleado')
    foto=models.ImageField(upload_to="fotos/", null= True, blank=True)
    nombres = models.CharField(max_length=30, verbose_name='Nombres')
    apellidos = models.CharField(max_length=30, verbose_name='Apellidos')
    ocupacion = models.ForeignKey(Ocupacion,  on_delete=CASCADE, verbose_name='Ocupacion')
    departamento = models.ForeignKey(Departamento, on_delete=CASCADE, verbose_name='Departamento')
    es_activo = models.BooleanField(default=True, verbose_name='Empleado esta activo')
    tiene_modelo=models.BooleanField(default=False,verbose_name='Registro de rostro para deteccion')
    # este modelo es el que lleva las caracteristicas del empleado 
    class Meta:
        db_table = 'empleado'
    def natural_key(self):
        return f'{self.carnet_empleado} {"-"}  {self.apellidos} {self.nombres}'
    
    def __str__(self):
        return f'{self.carnet_empleado} {"-"} {self.apellidos} {self.nombres}'  