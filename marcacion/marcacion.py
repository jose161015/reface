from datetime import datetime, timedelta
from empleado.models import*
from horarios.models import *
from marcacion.models import *
from evento.models import *
now = datetime.now()


def dia():
    semana = {1: 'Lunes', 2: 'Martes', 3: 'Miercoles',
              4: 'Jueves', 5: 'Viernes', 6: 'Sabado', 7: 'Domingo'}
    numero_dia = datetime.today().isoweekday()
    dia_n = semana[numero_dia]

    return dia_n

def registrarentrada(carnet):
    id_empleado=Empleado.objects.filter(carnet_empleado=carnet).first()                                              
    msg=""
    if id_empleado:
        if id_empleado.es_activo==True:
            horario=AsigHorario.objects.filter(empleado_id=id_empleado.id)
            now = datetime.now()
            fecha = now.strftime('%Y-%m-%d')
            if horario:
                for hora in horario:
                    if str(hora.fecha_inicio)<=str(fecha): 
                        if str(hora.fecha_fin)>=str(fecha):
                            nueva_entrada=[]
                            #aqui me quede 
                            turno = Turno.objects.filter(horario_id=hora.horario_id)
                            # si esta dentro del rango consultamos a turno los horarios de acuerdo al dia que se esta consultando
                            # en esta linea obtenemos el dia del dia
                            for t in turno:
                                # recorremos turno debido a que hay varios horarios con ese 
                                if t.dia == dia():
                                    # si el turno es igual a dia consultamos 
                                    ho = RangoHora.objects.get(id=t.rango_hora_id)
                                    #consultamos las horas
                                    tiempo=timedelta(hours=now.hour,minutes=now.minute,seconds=now.second)
                                    hora_add_entrada = timedelta(minutes=30) 
                                    hora_add_salida = timedelta(minutes=55)                   
                                    ini=ho.hora_inicio
                                    fin=ho.hora_fin
                                    hora_ini=timedelta(hours=ini.hour, minutes=ini.minute, seconds=ini.second)
                                    hora_fin=timedelta(hours=fin.hour, minutes=fin.minute, seconds=fin.second)
                                    if str(tiempo.seconds)>=str(hora_ini.seconds-hora_add_entrada.seconds):                                        
                                        if str(tiempo.seconds)<=str(hora_fin.seconds+hora_add_salida.seconds):
                                            #se agrega una hora a la hora de salida para la vigencia de la marcacion
                                            #si la hora que se consulta esta dentro del rango de la hora a marcar
                                            minutos_fin_mas=timedelta(hours=0, minutes=0, seconds=0)
                                            minutos_fin_menos=timedelta(hours=0, minutes=0, seconds=0)
                                            minutos_ini_mas=timedelta(hours=0, minutes=0, seconds=0)
                                            minutos_ini_menos=timedelta(hours=0, minutes=0, seconds=0)
                                            entrada_tardia=False
                                            salida_temprana=False
                                            # al realizar la resta cuando el resultado suele ser menos hay que hacer una
                                            # con timedelta resta
                                            nueva_entrada.append(ho.rango_hora)
                                            if str(tiempo-hora_ini)< "0":
                                                minutos_ini_mas=+(timedelta()-(tiempo-hora_ini))  
                                            else:
                                                minutos_ini_menos=tiempo-hora_ini
                                                entrada_tardia=True                                                                    
                                            if str(tiempo-hora_fin)<"0":
                                                minutos_fin_menos=+(timedelta()-(tiempo-hora_fin))
                                                salida_temprana=True                                                                    
                                            else:
                                                minutos_fin_mas=tiempo-hora_fin                                                                    
                                            # se consulta la tabla marcacion filtrada por la fecha de la marcacion
                                            # si hay registros del empleado que esta realizando la marcacion esto con el objeto 
                                            # marcar ya sea entrada o salida segun sea el caso
                                          
                                            #realizamos consulta en tabla marcacion para conocer si hay algun registro del dia 
                                            # del empleado
                                            consulta=Marcacion.objects.filter(fecha_marcacion=fecha)
                                            #iteramos la consulta
                                            lista=[]
                                            #esta lista se crea para llenarla con los id de registro de cada empleado
                                            if consulta:
                                                for iterar in consulta:
                                                    lista.append(str(iterar.empleado_id))                                                    
                                                    if iterar.empleado_id==id_empleado.id:
                                                        if ho.rango_hora==iterar.rango_horario:
                                                            if ho.rango_hora in nueva_entrada:
                                                                nueva_entrada.remove(ho.rango_hora)
                                                            #si hay un registro con el id del empleado consultamos la hora de entrada
                                                            hora_add_salida = timedelta(minutes=5)#minutos que se le sumaran 
                                                            # a hora entrada para que no sea una marcacion recurrente de entrada por salida
                                                            v_salida=iterar.hora_salida                                                                
                                                            if v_salida:
                                                                msg="Ya marco la salida de :",iterar.empleado
                                                            #si salida no tiene registro o esta vacio se procedera a realizar la actuyalizacion 
                                                            else:
                                                                entrada=iterar.hora_entrada
                                                                hora_entrada=timedelta(hours=entrada.hour, minutes=entrada.minute, seconds=entrada.second)
                                                                if str(tiempo.seconds)>str(hora_entrada.seconds+hora_add_salida.seconds):
                                                                    #si la hora actual es mayor a la hora de entrada mas los minutos extras definifos
                                                                    #entonces se procedera a realizar la actualizacion de ese registro
                                                                    Marcacion.objects.filter(empleado_id=id_empleado.id).update(
                                                                                                hora_salida=str(tiempo),
                                                                                                minutos_salida_mas=minutos_fin_mas,
                                                                                                minutos_salida_menos=minutos_fin_menos, 
                                                                                                salida_temprana=salida_temprana )
                                                                    msg="Salida marcada exitosamente de :",iterar.empleado
                                                if not str(id_empleado.id )in lista:
                                                    # si el id no esta en toda lista entonces se crea el registro 
                                                    # de una nueva marcacion
                                                    if ho.rango_hora in nueva_entrada:
                                                        nueva_entrada.remove(ho.rango_hora)
                                                    Marcacion.objects.create(
                                                                    empleado_id = id_empleado.id,
                                                                    horario_id=hora.horario_id,
                                                                    rango_horario=ho.rango_hora,
                                                                    fecha_marcacion=fecha,
                                                                    hora_entrada=str(tiempo),
                                                                    minutos_entrada_mas=str(minutos_ini_mas),
                                                                    minutos_entrada_menos=str(minutos_ini_menos),
                                                                    entrada_tardia=entrada_tardia)
                                                    msg="Entrada creada exitosamente de :",id_empleado
                                                elif ho.rango_hora in nueva_entrada:
                                                  
                                                    Marcacion.objects.create(
                                                                    empleado_id = id_empleado.id,
                                                                    horario_id=hora.horario_id,
                                                                    rango_horario=ho.rango_hora,
                                                                    fecha_marcacion=fecha,
                                                                    hora_entrada=str(tiempo),
                                                                    minutos_entrada_mas=str(minutos_ini_mas),
                                                                    minutos_entrada_menos=str(minutos_ini_menos),
                                                                    entrada_tardia=entrada_tardia)
                                                    msg="Nueva entrada creada exitosamente de :",id_empleado
                                                                                
                                            elif not consulta:
                                                Marcacion.objects.create(
                                                                empleado_id = id_empleado.id,
                                                                horario_id=hora.horario_id,
                                                                rango_horario=str(ho.rango_hora),
                                                                fecha_marcacion=fecha,
                                                                hora_entrada=str(tiempo),
                                                                minutos_entrada_mas=minutos_ini_mas,
                                                                minutos_entrada_menos=minutos_ini_menos,
                                                                entrada_tardia=entrada_tardia
                                                                                           )   
                                                msg="Entrada creada exitosamente de :",id_empleado
                                    else:
                                        msg="Todavia no es hora de marcar",id_empleado
                                    
                        else:
                            msg="Horario caducado para :",id_empleado
                else:
                    msg="sin asignacion de horario para :",id_empleado
        else:
            msg=id_empleado,"--> esta inactivo"
    else:
        msg="Empleado con numero de carnet :",carnet," NO existe" 
    return msg




def monitor_ausencia(): 
    w = datetime.now()
    fecha = w.strftime('%Y-%m-%d')
    hora_actual = timedelta(hours=w.hour, minutes=w.minute, seconds=w.second)
    falto=True
    vacacion=False
    permiso=False
    
    #se hara recorrido en la plantilla de empleados para verificar si hay inasistencia en el dia 
    marcacion_dia=Marcacion.objects.filter(fecha_marcacion=fecha)
    empleado=Empleado.objects.all()
    
    if marcacion_dia:
        for em in empleado:
            #se hace un recorrido de todos los empleados
            asig=AsigHorario.objects.filter(empleado_id=em.id)
            print("asignacion de horarios")
            if asig.count()>1:
                for g in asig:
                    turno=Turno.objects.filter(horario_id=g.horario_id)
                    for t in turno:
                        # recorremos turno debido a que hay varios horarios con ese 
                        if t.dia == dia():
                            # si el dia que consultamos no esta en el turno correspondiente no hara nada
                            # si el turno es igual a dia que consultamos 
                            ho = RangoHora.objects.get(id=t.rango_hora_id)
                            for m in marcacion_dia:
                                if m.empleado_id==em.id:
                                    if m.rango_horario==ho.rango_hora:
                                        falto=False
                            if falto==True:
                                fin=ho.hora_fin
                                hora_fin=timedelta(hours=fin.hour, minutes=fin.minute, seconds=fin.second)
                                if hora_actual.seconds>hora_fin.seconds:
                                    evento=Evento.objects.filter(empleado_id=em.id)
                                    #se verifica si triene algun evento que le autorise ausentarse de la hora laboral
                                    if evento:
                                        if evento.count()>1:
                                            for e in evento:
                                                if str(fecha)>=str(e.fecha_inicio):
                                                    if str(fecha)<=str(e.fecha_fin):
                                                        #si el evento existe el permiso es verdadero de lo contrario 
                                                        # se mantendra falso
                                                        permiso=True
                                        else:
                                            event=Evento.objects.get(empleado_id=em.id)
                                            if str(fecha)>=str(event.fecha_inicio):
                                                if str(fecha)<=str(event.fecha_fin):
                                                    permiso=True
                                    if permiso==False:
                                        #si no hay evento activo que le permita faltar hay que consultar si hay asueto activo
                                        asu=Asueto.objects.all()
                                        for a in asu:
                                            if str(fecha)>=str(a.fecha_inicio):
                                                if str(fecha)<=str(a.fecha_finalizacion):
                                                    h=Horario.objects.filter(id=g.horario_id)
                                                    for d in a.tipohorario.all():
                                                        if h.tipohorario_id==d.id:
                                                            vacacion=True
                                    if vacacion==False:
                                        registrar=True
                                        ausencia=Ausencias.objects.filter(fecha=fecha)
                                        if ausencia:
                                            for au in ausencia:
                                                if au.empleado_id==em.id:
                                                    if au.rango_hora==ho.rango_hora:
                                                        registrar=False
                                                        print("ya tiene registro ausencia",au.rango_hora)
                                        elif registrar==True:
                                            Ausencias.objects.create(rango_hora=ho.rango_hora,fecha=fecha,empleado_id=em.id,horario_id=g.horario_id)                                                            
            else:
                asi=AsigHorario.objects.get(empleado_id=em.id)
                turno=Turno.objects.filter(horario_id=asi.horario_id)
                for t in turno:
                    # recorremos turno debido a que hay varios horarios con ese 
                    if t.dia == dia():
                        #si el dia que consultamos no esta en el turno correspondiente no hara nada
                        # si el turno es igual a dia que consultamos 
                        ho = RangoHora.objects.get(id=t.rango_hora_id)
                        for m in marcacion_dia:
                            if m.empleado_id==em.id:
                                if m.rango_horario==ho.rango_hora:
                                    falto=False
                                    print("Se presento a trabajar")
                        if falto==True:
                            print("no se presento a trabajar")
                            fin=ho.hora_fin
                            hora_fin=timedelta(hours=fin.hour, minutes=fin.minute, seconds=fin.second)
                            if hora_actual.seconds>hora_fin.seconds:
                                evento=Evento.objects.filter(empleado_id=em.id)
                                #se verifica si triene algun evento que le autorise ausentarse de la hora laboral
                                if evento:
                                    if evento.count()>1:
                                        for e in evento:
                                            if str(fecha)>=str(e.fecha_inicio):
                                                if str(fecha)<=str(e.fecha_fin):
                                                    #si el evento existe el permiso es verdadero de lo contrario 
                                                    # se mantendra falso
                                                    permiso=True
                                                    print("Tiene permiso")
                                    else:
                                        event=Evento.objects.get(empleado_id=em.id)
                                        if str(fecha)>=str(event.fecha_inicio):
                                            if str(fecha)<=str(event.fecha_fin):
                                                permiso=True
                                                print("Tiene permiso")
                                if permiso==False:
                                    #si no hay evento activo que le permita faltar hay que consultar si hay asueto activo
                                    asu=Asueto.objects.all()
                                    for a in asu:
                                        if str(fecha)>=str(a.fecha_inicio):
                                            if str(fecha)<=str(a.fecha_finalizacion):
                                                h=Horario.objects.filter(id=asi.horario_id)
                                                for d in a.tipohorario.all():
                                                    if h.tipohorario_id==d.id:
                                                        vacacion=True
                                                        print("Es asueto")
                                if vacacion==False:
                                    registrar=True
                                    ausencia=Ausencias.objects.filter(fecha=fecha)
                                    if ausencia:
                                        for au in ausencia:
                                            if au.empleado_id==em.id:
                                                if au.rango_hora==ho.rango_hora:
                                                    registrar=False
                                                    print("ya tiene registro ausencia",au.rango_hora)
                                    elif registrar==True:
                                        Ausencias.objects.create(rango_hora=ho.rango_hora,fecha=fecha,empleado_id=em.id,horario_id=g.horario_id)
    else:
        for em in empleado:
            #se hace un recorrido de todos los empleados
            asig=AsigHorario.objects.filter(empleado_id=em.id)
            print("asignacion de horarios")
            if asig.count()>1:
                for g in asig:
                    turno=Turno.objects.filter(horario_id=g.horario_id)
                    for t in turno:
                        # recorremos turno debido a que hay varios horarios con ese 
                        if t.dia == dia():
                            # si el dia que consultamos no esta en el turno correspondiente no hara nada
                            # si el turno es igual a dia que consultamos 
                            ho = RangoHora.objects.get(id=t.rango_hora_id)
                            if falto==True:
                                fin=ho.hora_fin
                                hora_fin=timedelta(hours=fin.hour, minutes=fin.minute, seconds=fin.second)
                                if hora_actual.seconds>hora_fin.seconds:
                                    evento=Evento.objects.filter(empleado_id=em.id)
                                    #se verifica si triene algun evento que le autorise ausentarse de la hora laboral
                                    if evento:
                                        if evento.count()>1:
                                            for e in evento:
                                                if str(fecha)>=str(e.fecha_inicio):
                                                    if str(fecha)<=str(e.fecha_fin):
                                                        #si el evento existe el permiso es verdadero de lo contrario 
                                                        # se mantendra falso
                                                        permiso=True
                                        else:
                                            event=Evento.objects.get(empleado_id=em.id)
                                            if str(fecha)>=str(event.fecha_inicio):
                                                if str(fecha)<=str(event.fecha_fin):
                                                    permiso=True
                                    if permiso==False:
                                        #si no hay evento activo que le permita faltar hay que consultar si hay asueto activo
                                        asu=Asueto.objects.all()
                                        for a in asu:
                                            if str(fecha)>=str(a.fecha_inicio):
                                                if str(fecha)<=str(a.fecha_finalizacion):
                                                    h=Horario.objects.filter(id=g.horario_id)
                                                    for d in a.tipohorario.all():
                                                        if h.tipohorario_id==d.id:
                                                            vacacion=True
                                    if vacacion==False:
                                        registrar=True
                                        ausencia=Ausencias.objects.filter(fecha=fecha)
                                        if ausencia:
                                            for au in ausencia:
                                                if au.empleado_id==em.id:
                                                    if au.rango_hora==ho.rango_hora:
                                                        registrar=False
                                                        print("ya tiene registro ausencia",au.rango_hora)
                                        elif registrar==True:
                                            Ausencias.objects.create(rango_hora=ho.rango_hora,fecha=fecha,empleado_id=em.id,horario_id=g.horario_id)                                                            
            else:
                asi=AsigHorario.objects.get(empleado_id=em.id)
                turno=Turno.objects.filter(horario_id=asi.horario_id)
                for t in turno:
                    # recorremos turno debido a que hay varios horarios con ese 
                    if t.dia == dia():
                        #si el dia que consultamos no esta en el turno correspondiente no hara nada
                        # si el turno es igual a dia que consultamos 
                        ho = RangoHora.objects.get(id=t.rango_hora_id)
                        if falto==True:
                            print("no se presento a trabajar")
                            fin=ho.hora_fin
                            hora_fin=timedelta(hours=fin.hour, minutes=fin.minute, seconds=fin.second)
                            if hora_actual.seconds>hora_fin.seconds:
                                evento=Evento.objects.filter(empleado_id=em.id)
                                #se verifica si triene algun evento que le autorise ausentarse de la hora laboral
                                if evento:
                                    if evento.count()>1:
                                        for e in evento:
                                            if str(fecha)>=str(e.fecha_inicio):
                                                if str(fecha)<=str(e.fecha_fin):
                                                    #si el evento existe el permiso es verdadero de lo contrario 
                                                    # se mantendra falso
                                                    permiso=True
                                                    print("Tiene permiso")
                                    else:
                                        event=Evento.objects.get(empleado_id=em.id)
                                        if str(fecha)>=str(event.fecha_inicio):
                                            if str(fecha)<=str(event.fecha_fin):
                                                permiso=True
                                                print("Tiene permiso")
                                if permiso==False:
                                    #si no hay evento activo que le permita faltar hay que consultar si hay asueto activo
                                    asu=Asueto.objects.all()
                                    for a in asu:
                                        if str(fecha)>=str(a.fecha_inicio):
                                            if str(fecha)<=str(a.fecha_finalizacion):
                                                h=Horario.objects.filter(id=asi.horario_id)
                                                for d in a.tipohorario.all():
                                                    if h.tipohorario_id==d.id:
                                                        vacacion=True
                                                        print("Es asueto")
                                if vacacion==False:
                                    registrar=True
                                    ausencia=Ausencias.objects.filter(fecha=fecha)
                                    if ausencia:
                                        for au in ausencia:
                                            if au.empleado_id==em.id:
                                                if au.rango_hora==ho.rango_hora:
                                                    registrar=False
                                                    print("ya tiene registro ausencia",au.rango_hora)
                                    elif registrar==True:
                                        Ausencias.objects.create(rango_hora=ho.rango_hora,fecha=fecha,empleado_id=em.id,horario_id=g.horario_id)
    return 
