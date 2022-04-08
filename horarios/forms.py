from django import forms
from django.forms import models
from horarios.models import AsigHorario,Asueto, TipoHorario

class Asighorarioform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Asighorarioform, self).__init__(*args, **kwargs)

        self.fields['empleado'].widget.attrs = {
            'class': 'form-control form-control-line'
        }
        self.fields['horario'].widget.attrs = {
            'class': 'form-control form-control-line'
        }
        self.fields['fecha_inicio'].widget.attrs = {
            'class': 'form-control form-control-line',
            
        }
        self.fields['fecha_fin'].widget.attrs = {
            'class': 'form-control form-control-line',
            
        }
    class Meta:
        model = AsigHorario
        fields = ['empleado','horario','fecha_inicio','fecha_fin',
                  ]
        labels = {
            'empleado': 'Empleado que se asignara horario',
            'horario': 'Horario a asignacion',
            'fecha_inicio':'Fecha de inicio',
            'fecha_fin':'Fecha de finalizacion',
            
        }
        widgets = {            
            'fecha_inicio': forms.DateInput(
                attrs = {
                    'type':'date',
                    'class':'form-control',
                    
                }
            ),
            'fecha_fin': forms.DateInput(
                attrs = {
                    'type':'date',
                    'class':'form-control',
                    
                }
            ), 
        }
class Asuetoform(models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Asuetoform, self).__init__(*args, **kwargs)
        self.fields['nombre_asueto'].widget.attrs = {
            'class': 'form-control form-control-line'
        }
        self.fields['fecha_inicio'].widget.attrs = {
            'class': 'form-control form-control-line'
        }
        self.fields['fecha_finalizacion'].widget.attrs = {
            'class': 'form-control form-control-line',
            
        }
        self.fields['tipohorario'].widget.attrs = {
            'class': 'form-control form-control-line',
            
        }
    class Meta:
        model = Asueto
        fields=['nombre_asueto','fecha_inicio','fecha_finalizacion','tipohorario']
        
        labels = {
            'nombre_asueto': 'Nombre del asueto a registrar',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_finalizacion':'Fecha de finalizacion',
            'tipohorario':'Tipos de horarios agregados al asueto',            
        }
        widgets = { 
            'nombre_asueto': forms.TextInput(
                attrs = {
                    'type':'text',
                    'class':'form-control',
                    
                }
            ),           
            'fecha_inicio': forms.DateInput(
                attrs = {
                    'type':'date',
                    'class':'form-control',
                    
                }
            ),
            'fecha_finalizacion': forms.DateInput(
                attrs = {
                    'type':'date',
                    'class':'form-control',
                    
                }
            ), 
            'tipohorario': forms.SelectMultiple(
                attrs = {
                    'class':'form-control'
                }
            ),
        }
            