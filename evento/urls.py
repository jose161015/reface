from django.urls import path
from evento.views import *
urlpatterns = [
	path('menuevento', menu_evento, name='menu_evento'),
    path('regevento', regevento, name='reg_evento'),
    path('regcodevento', regcodevento, name='regcodevento'),
    path('listarevento',listarevento,name='listarevento'),
    path('editarevento/<int:id>',editarevento,name='editarevento'),
    path('actualizar',actualizarevento,name='actualizar'),
    path('eventorango',eventorango,name='eventorango'),
    path('eventorangopdf',eventorangopdf,name='eventorangopdf'),


]