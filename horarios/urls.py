from django.urls import path
from horarios.views import*

urlpatterns = [
        path('horarios', menu_horarios, name='menu_horarios'),
        path('listarangohoras',listrangohoras,name='listrangohoras'),
        path('regrangohoras',regrangohoras,name='regrangohoras'),
        path('editarhoras/<int:id>',editarhoras,name='editarhoras'),
        path('actualizar',actualizarhoras,name='actualizarhoras'),
        path('regtipohorario',regtipohorarios,name='regtipohorario'),
        path('editartipohorario/<int:id>',editartipohorarios,name='editartipohorario'),
        path('actualizartipohorario',actualizartipohorario,name='actualizartipohorario'),
        path('listhorario',listhorarios, name='listhorario'),
        path('editarhorario/<int:id>',editarhorarios, name='editarhorario'),
        path('actualizarhorario',actualizarhorario, name='actualizarhorario'),
        path('listurnos',listurno,name='listurno'),
        path('regturno/<int:id>',regturno,name='regturno'),
        path('guardarturno',guardarturno, name='guardarturno'),
        path('editarturno/<int:id>',editarturno,name='editarturno'),
        path('actualizarturno',actualizarturno,name='actualizarturno'),
        path('listasighorarios',listasignarhorario,name='listasignarhorarios'),
        path('asignarhorarios',asignarhorario, name='asignarhorarios'),
        path('asighorariodetail/<int:pk>',AsignarhorarioDetail.as_view(), name='asighorariodetail'),
        path('asighorarioeditar/<int:pk>',AsighorarioUpdate.as_view(), name='asighorarioeditar'),
        path('asuetolist', AsuetoList, name='asuetolist'),
        path('asuetodetail/<int:pk>',AsuetoDetail.as_view(),name='asuetodetail'),
        path('asuetocreate', AsuetoCreate.as_view(),name='asuetocreate'),
        path('asuetoupdate/<int:pk>',AsuetoUpdate.as_view(),name='asuetoupdate')
        
]