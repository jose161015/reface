from os import name
from django.urls import path
from empleado.views import *

urlpatterns = [
        path('menu_empleado', menu_empleado, name='menu_empleado'),
        path('reg_empleado', registrar_empleado, name='registrarempleado'),
        path('reg_departamento', reg_departamento, name='registrardepartamento'),
        path('deptdetail/<int:id>',deptdetail,name='deptdetail'),
        path('actualizardpt',actualizardpt,name='actualizardpt'),
        path('ocpdetail/<int:id>',ocpdetail,name='ocpdetail'),
        path('reg_ocupacion', reg_ocupacion, name='registrarocupacion'),
        path('actualizarocupacion',actualizarocupacion, name='actualizarocupacion'),
        path('listempleado_sin', lista_sin_captura, name='listasincaptura'),
        path('empleadodetalle', detalle_empleado, name='empleadodetalle'),
        path('listarempleado', listarempleado, name='listaempleado'),
        path('dar_de_baja/<int:id>', dar_de_baja, name='dar_de_baja'),
        path('dar_de_alta/<int:id>', dar_de_alta, name='dar_de_alta'),
        path('editarempleado/<int:id>', editarempleado, name='editarempleado'),
        path('actualizarempleado',actualizarempleado, name='actualizarempleado'),
        
        
        
    ]
