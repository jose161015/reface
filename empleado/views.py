from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from empleado.models import Departamento,Ocupacion,Empleado
from horarios.models import AsigHorario, Turno
from marcacion.models import*
from empleado.Registro import entrenar
import numpy as np
import os

import cv2

# Create your views here.

def menu_empleado(request):
    return render(request, 'empleado/menu_empleado/menu_empleado.html')


def registrar_empleado(request):
    departamento=Departamento.objects.all()
    ocupacion=Ocupacion.objects.all()
    if request.method=="POST":
        carnet=request.POST['carnet']
        nombre=request.POST['nombre']
        apellido=request.POST['apellido']
        dept=request.POST['departamento']
        oc=request.POST['ocupacion']
        depart=Departamento.objects.get(id=dept)
        ocu=Ocupacion.objects.get(id=oc)
        try:
            Empleado.objects.create(carnet_empleado=carnet,
                                    nombres=nombre,apellidos=apellido, 
                                    departamento=depart,ocupacion=ocu)
            return redirect('menu_empleado')
        except Exception as ms:
            print (ms)
            return render(request,'empleado/reg_empleado/registrar_empleado.html',{'departamento':departamento,'ocupacion':ocupacion,'msg':"Carnet ya se encuentra registrado consulte con el administrador"}) 
    return render(request,'empleado/reg_empleado/registrar_empleado.html',{'departamento':departamento,'ocupacion':ocupacion})

def reg_departamento(request):
    departamento=Departamento.objects.all()
    if request.method=='POST':
        dept=request.POST['dpt']
        Departamento.objects.create(nom_departamento=dept)
        return redirect('registrardepartamento')
    return render(request,'empleado/reg_dept/registrodepartamento.html',{'departamento':departamento})


def deptdetail(request,id):
    detail=Departamento.objects.get(id=id)
    return render(request,'empleado/deptdetail/dpt.html',{'detail':detail})


def actualizardpt(request):
    if request.method=='POST':
        id=request.POST['id']
        nom=request.POST['nom']
        Departamento.objects.filter(id=id).update(nom_departamento=nom)
        return redirect('registrardepartamento')


def listarempleado(request):
    empleado=Empleado.objects.all()
    return render(request,'empleado/listarempleado/listar_empleado.html',{'empleado':empleado,'count':empleado.count()})


def dar_de_baja(request, id):
    Empleado.objects.filter(id=id).update(es_activo=False)
    return redirect('listaempleado')


def dar_de_alta(request, id):
    Empleado.objects.filter(id=id).update(es_activo=1)
    return redirect('listaempleado')

def editarempleado(request, id):
    departamento=Departamento.objects.all()
    ocupacion=Ocupacion.objects.all()
    empleado=Empleado.objects.filter(id=id).first()
    return render(request,'empleado/editarempleado/actualizar_empleado.html',{'empleado':empleado,'departamento':departamento,'ocupacion':ocupacion})


def actualizarempleado(request):
    if request.method=='POST':
        nombre=request.POST['nombre']
        apellido=request.POST['apellido']
        dept=request.POST['departamento']
        ocup=request.POST['ocupacion']
        carnet=request.POST['carnet']
        Empleado.objects.filter(carnet_empleado=carnet).update(nombres=nombre,
                                                                apellidos=apellido,departamento=dept,ocupacion=ocup) 
    return redirect('menu_empleado')






def reg_ocupacion(request):
    ocupacion=Ocupacion.objects.all()
    if request.method=='POST':
        ocup=request.POST['ocp']
        Ocupacion.objects.create(nom_ocupacion=ocup)
        return redirect('registrarocupacion')
    return render(request, 'empleado/reg_ocupacion/registroocupacion.html',{'ocupacion':ocupacion})


def ocpdetail(request,id):
    ocp=Ocupacion.objects.get(id=id)
    return render(request,'empleado/ocpdetail/ocpdetail.html',{'ocp':ocp})


def actualizarocupacion(request):
    if request.method=='POST':
        id=request.POST['id']
        nom=request.POST['nom']
        Ocupacion.objects.filter(id=id).update(nom_ocupacion=nom)
        return redirect('registrarocupacion')


def lista_sin_captura(request):
    listasincaptura=Empleado.objects.filter(tiene_modelo=0)
    return render(request, 'empleado/listempleado_sin/listasincaptura.html',{'listasincaptura':listasincaptura})





#--------------------------------------------------------------------------------------------------------------------------
def captura_rostro(request,id):
    coreDatos = os.getcwd()
    pathcore = os.path.join(coreDatos,"media")
    path = os.path.join(pathcore,"fotos_empleados")
    if not os.path.isdir(pathcore):
        os.mkdir(pathcore)
        print("Se creo la carpeta CoreDatos")
        #Si no hay una carpeta con el nombre ingresado entonces se crea
    if not os.path.isdir(path):
        os.mkdir(path)  
    e=Empleado.objects.filter(id=id).first()
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
    while(True):
        ret,frame = cap.read() # return a single frame in variable `frame`
        cv2.imshow("toma de imagen: ("+str(e)+") Presione ( y ) para capturar",frame) #display the captured image
        if cv2.waitKey(1) & 0xFF == ord("y"): #save on pressing "y"
            cv2.imwrite('%s/%s.png' % (path,id),frame)
            cv2.destroyAllWindows()
            foto="fotos_empleados/"+str(id)+".png"
            Empleado.objects.filter(id=id).update(foto=foto)
            break

    cap.release()
    return redirect('listasincaptura')

#------------------------------ se ejecuta despues de captura rostro-----------------------------
def entrenamiento(request,id):
    e=Empleado.objects.filter(id=id).first()
    carnet=e.carnet_empleado
    nombre=e.nombres
    cantidadimagenes=150
    dir_faces = os.getcwd()
    path = os.path.join(dir_faces,carnet)
    size = 4
    coreDatos = os.getcwd()
    pathcore = os.path.join(coreDatos,"CoreDatos")
    path = os.path.join(pathcore,carnet)
    print("Ruta actual: " + path)
    if not os.path.isdir(pathcore):
        os.mkdir(pathcore)
        print("Se creo la carpeta CoreDatos")
        #Si no hay una carpeta con el nombre ingresado entonces se crea
    if not os.path.isdir(path):
        os.mkdir(path)
        print("Se creo la base de imagenes: " + carnet)
        #cargamos la plantilla e inicializamos la webcam
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    img_width, img_height = 100, 100
    print("Registrando su rostro...")
    #Ciclo para tomar fotografias
    while True: #captura imagenes
        #leemos un frame y lo guardamos
        rval, img = cap.read()
        img = cv2.flip(img, 1,0)
            #convertimos la imagen a blanco y negro
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #redimensionar la imagen
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        """buscamos las coordenadas de los rostros (si los hay) y
        guardamos su posicion"""
        faces = face_cascade.detectMultiScale(mini)    
        faces = sorted(faces, key=lambda x: x[3])
        if faces:
            face_i = faces[0]
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (img_width, img_height))
            #Dibujamos un rectangulo en las coordenadas del rostro
            coreDatos = os.getcwd()
            pathcore = os.path.join(coreDatos, "CoreDatos")
            path = os.path.join(pathcore, carnet)
            cantimgs = len(os.listdir(path))
            if cantimgs < cantidadimagenes: 
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    #Ponemos el nombre en el rectagulo
                cv2.putText(img, nombre, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 255))        
                    #El nombre de cada foto es el numero del ciclo
                    #Obtenemos el nombre de la foto
                    #Despues de la ultima sumamos 1 para continuar con los demas nombres
                pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
                        if n[0]!='.' ]+[0])[-1] + 1        #Metemos la foto en el directorio
                cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
            else:
                cv2.putText(img, 'Finish, press Q to quit', (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0),2)
            #Mostramos la imagen
        cv2.imshow('Registrando rostro de: '+nombre, img)
            #Si se presiona la tecla ESC se cierra el programa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            entrenar()
            Empleado.objects.filter(id=id).update(tiene_modelo=1)
            break
    cap.release()
    cv2.destroyAllWindows()
    
    return redirect('listasincaptura')
#------------------------------- solo toma foto--------------------------
def tomarfoto(request,id):
    coreDatos = os.getcwd()
    pathcore = os.path.join(coreDatos,"media")
    path = os.path.join(pathcore,"fotos_empleados")
    if not os.path.isdir(pathcore):
        os.mkdir(pathcore)
        print("Se creo la carpeta CoreDatos")
        #Si no hay una carpeta con el nombre ingresado entonces se crea
    if not os.path.isdir(path):
        os.mkdir(path)  
    e=Empleado.objects.filter(id=id).first()
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
    while(True):
        ret,frame = cap.read() # return a single frame in variable `frame`
        cv2.imshow("toma de imagen: ("+str(e)+") Presione ( y ) para capturar",frame) #display the captured image
        if cv2.waitKey(1) & 0xFF == ord("y"): #save on pressing "y"
            cv2.imwrite('%s/%s.png' % (path,id),frame)
            cv2.destroyAllWindows()
            foto="fotos_empleados/"+str(id)+".png"
            Empleado.objects.filter(id=id).update(foto=foto)
            break

    cap.release()
    return redirect('editarempleado',id)






def detalle_empleado(request):
    if request.method=='GET':
        if request.GET['id']!="":
            id=request.GET['id']
            empleado=Empleado.objects.filter(carnet_empleado=id).first()
            if empleado:
                ausencia=[]
                tur=[]
                cuenta=0
                tardias=[]
                lunes=[]
                martes=[]
                miercoles=[]
                jueves=[]
                viernes=[]
                sabado=[]
                domingo=[]
                try:
                    asig=AsigHorario.objects.filter(empleado_id=empleado.id)
                    if asig.count()>1:
                        for asi in asig:
                            turno=Turno.objects.filter(horario_id=asi.horario_id)
                            print(cuenta)
                            
                            
                            for t in turno:
                                
                                if t.dia=="Lunes":
                                    tur.append(t.horario)
                                    lunes.append(t.rango_hora)                 
                                elif t.dia=="Martes":
                                    martes.append(t.rango_hora)                
                                elif t.dia=="Miercoles":
                                    miercoles.append(t.rango_hora)              
                                elif t.dia=="Jueves":
                                    jueves.append(t.rango_hora)
                                elif t.dia=="Viernes":
                                    viernes.append(t.rango_hora)              
                                elif t.dia=="Sabado":
                                    sabado.append(t.rango_hora)               
                                elif t.dia=="Domingo":
                                    domingo.append(t.rango_hora)
                            
                        print (turno)
                        ausencia=Ausencias.objects.filter(empleado_id=empleado.id).exclude(esta_faltando=0)
                        tardias=Marcacion.objects.filter(empleado_id=empleado.id).filter(Q(entrada_tardia=1)|Q(salida_temprana=1))        
                        return render(request, 'empleado/empleadodetalle/empleadodetalle.html',{'empleado':empleado,'asig':asig,'tur':tur,
                                                                            'lunes':lunes,'martes':martes,'miercoles':miercoles,
                                                                            'jueves':jueves,'viernes':viernes,'sabado':sabado,
                                                                            'domingo':domingo,'ausencia':ausencia,'tardias':tardias,'asigcount':asig.count()})
                    else:
                        asig=AsigHorario.objects.get(empleado_id=empleado.id)
                        turno=Turno.objects.filter(horario_id=asig.horario_id)
                        for t in turno:
                            print(t)
                            if t.dia=="Lunes":
                                lunes.append(t.rango_hora)                 
                            elif t.dia=="Martes":
                                martes.append(t.hora)                
                            elif t.dia=="Miercoles":
                                miercoles.append(t.hora)              
                            elif t.dia=="Jueves":
                                jueves.append(t.hora)
                            elif t.dia=="Viernes":
                                viernes.append(t.hora)              
                            elif t.dia=="Sábado":
                                sabado.append(t.hora)               
                            elif t.dia=="Domingo":
                                domingo.append(t.hora)
                        print(asig.horario)   
                        ausencia=Ausencias.objects.filter(empleado_id=empleado.id).exclude(esta_faltando=0)
                        tardias=Marcacion.objects.filter(empleado_id=empleado.id).filter(Q(entrada_tardia=1)|Q(salida_temprana=1))        
                        return render(request, 'empleado/empleadodetalle/empleadodetalle.html',{'empleado':empleado,'asig':asig,
                                                                            'lunes':lunes,'martes':martes,'miercoles':miercoles,
                                                                            'jueves':jueves,'viernes':viernes,'sabado':sabado,
                                                                            'domingo':domingo,'ausencia':ausencia,'tardias':tardias,'asigcount':asig.count()})
                except:
                    ausencia=Ausencias.objects.filter(empleado_id=empleado.id).exclude(esta_faltando=0)
                    tardias=Marcacion.objects.filter(empleado_id=empleado.id).filter(Q(entrada_tardia=1)|Q(salida_temprana=1))
                    return render(request, 'empleado/empleadodetalle/empleadodetalle.html',{'empleado':empleado,'asig':asig,
                                                                            'lunes':lunes,'martes':martes,'miercoles':miercoles,
                                                                            'jueves':jueves,'viernes':viernes,'sabado':sabado,'domingo':domingo,
                                                                            'ausencia':ausencia,'tardias':tardias, 'asigcount':asig.count()})   
        else:
            return render(request, 'index.html',{'error':'Solicitud no procesada'})
    