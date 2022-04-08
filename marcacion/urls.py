from django.urls import path

from marcacion.views import *

urlpatterns = [
    path('menu_marcaciones',menu_marcaciones,name='menu_marcaciones'),
    path('listar_marcacion',listar_marcacion, name='listarmarcacion'),
    path('marcacion_manual',marcacionmanualentrada, name='marcacionmanualentrada'),
    path('tardiasytemprana',entradatardia_o_salidatemprana,name='entradas_o_salidas_tempranas'),
    path('justificar/<int:id>',justificar, name='justificar'),
    path('actualizarmarcacion', actualizarmarcacion, name='actualizarmarcacion'),
    path('listaausencias', listaausencias, name='lista_ausencias'),
    path('detalleausencia/<int:id>',detalleausencia, name='detalleausencia'),
    path('actualizarausencia',actualizarausencia,name='actualizarausencia'),
    path('reconocimientofacial', reconocimientofacial,name='reconocimientofacial'),
    path('minutostarde',tardias_rango_fecha, name='sumaminutostarde'),
    path('descargaexcel',excelausencias, name='descargaexcel'),
    path('reg_camara_ip', reg_camara_ip, name='reg_camara_ip' ),
    path('index', recibir_url, name='recibir_url' ),
    ]