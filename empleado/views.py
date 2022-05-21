from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Q
from empleado.models import Departamento,Ocupacion,Empleado
from horarios.models import AsigHorario, Turno
from marcacion.models import*
from empleado.Registro import entrenar
import os
from datetime import datetime
import cv2


def menu_empleado(request):
    return render(request, 'empleado/menu_empleado/menu_empleado.html')

def registrar_empleado(request):
    departamento=Departamento.objects.all()
    ocupacion=Ocupacion.objects.all()
    if request.method=="POST":
        dept=request.POST['departamento']
        oc=request.POST['ocupacion']
        if dept!="Elegir departamento":
            if oc!="Elegir ocupacion":
                carnet=request.POST['carnet']
                empleado=Empleado.objects.filter(carnet_empleado=carnet)
                if empleado.exists():
                    render(request,'empleado/reg_empleado/registrar_empleado.html',
                                  {'departamento':departamento,'ocupacion':ocupacion,
                                   'msg':"Carnet ya se encuentra registrado consulte con el administrador"})
                else:
                    dir_faces = os.getcwd()
                    myfile = request.FILES['image']
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    
                    uploaded_file_url = fs.url(filename)
                    
                    full_url=dir_faces+"/"+uploaded_file_url[1:]

                    path_to_image=full_url
                    cascPath=dir_faces+"/"+"haarcascades/haarcascade_frontalface_default.xml"
                    original_image = cv2.imread(path_to_image)
                    if original_image is not None:
                        
                        faceCascade=cv2.CascadeClassifier(cascPath)
                        gray=cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY)
                        faces=faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                        
                        if len(faces)<=0:
                            os.remove(full_url)
                            return render(request,'empleado/reg_empleado/registrar_empleado.html',{'departamento':departamento,
                                                                                                   'ocupacion':ocupacion,
                                                                                                   'msg':"No habia ningun rostro en imagen por favor elija una imagen con rostro visible y de calidad"})
                        elif len(faces)>1:
                            os.remove(full_url)
                            return render(request,'empleado/reg_empleado/registrar_empleado.html',{'departamento':departamento,
                                                                                                   'ocupacion':ocupacion,
                                                                                                   'msg':"Habia mas de un rostro en imagen por favor elija una imagen con rostro visible y de la persona que registra, asegurese que el fondo de la imagen este limpio"})
                        else:
                            img_width, img_height = 500, 500
                            size = 6
                            pathcore = os.path.join(dir_faces, "CoreDatos")
                            path = os.path.join(pathcore, carnet)
                            if not os.path.isdir(pathcore):
                                os.mkdir(pathcore)
                                
                                # Si no hay una carpeta con el nombre ingresado entonces se crea
                            if not os.path.isdir(path):
                                os.mkdir(path)
                                
                            mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
                            faces1 = faceCascade.detectMultiScale(mini)    
                            faces1 = sorted(faces1, key=lambda x: x[3])
                            face_i = faces1[0]
                            (x, y, w, h) = [v * size for v in face_i]
                            face1 = gray[y:y + h, x:x + w]
                            face_resize = cv2.resize(face1, (img_width, img_height))
                            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 1)
                                 #Ponemos el nombre en el rectagulo
                            cv2.putText(original_image, carnet, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 255))        
                               
                                #Obtenemos el nombre de la foto
                                #Despues de la ultima sumamos 1 para continuar con los demas nombres
                            pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
                            if n[0]!='.' ]+[0])[-1] + 1        #Metemos la foto en el directorio
                            cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
                            entrenar()
                            
                            nombre=request.POST['nombre']
                            apellido=request.POST['apellido']
                            dept=request.POST['departamento']
                            oc=request.POST['ocupacion']
                            depart=Departamento.objects.get(id=dept)
                            ocu=Ocupacion.objects.get(id=oc)
                            Empleado.objects.create(carnet_empleado=carnet,
                                                nombres=nombre,
                                                apellidos=apellido, 
                                                departamento=depart,
                                                ocupacion=ocu,
                                                foto=filename,
                                                tiene_modelo=True)
                            return redirect('menu_empleado')
            else:
                return render(request,'empleado/reg_empleado/registrar_empleado.html',{'departamento':departamento,'ocupacion':ocupacion,'msg':"Debe elegir ocupacion que desempeña"})
        else:
            return render(request,'empleado/reg_empleado/registrar_empleado.html',{'departamento':departamento,'ocupacion':ocupacion,'msg':"Debe elegir departamento de pertenencia"})
                    
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

@never_cache
def listarempleado(request):
    time=datetime.now()
    empleado=Empleado.objects.all()
    return render(request,'empleado/listarempleado/listar_empleado.html',{'empleado':empleado,'count':empleado.count(),'time':time})


def dar_de_baja(request, id):
    Empleado.objects.filter(id=id).update(es_activo=False)
    return redirect('listaempleado')


def dar_de_alta(request, id):
    Empleado.objects.filter(id=id).update(es_activo=1)
    return redirect('listaempleado')
@never_cache
def editarempleado(request, id):
    time=datetime.now()
    departamento=Departamento.objects.all()
    ocupacion=Ocupacion.objects.all()
    empleado=Empleado.objects.filter(id=id).first()
    return render(request,'empleado/editarempleado/actualizar_empleado.html',{'empleado':empleado,'departamento':departamento,'ocupacion':ocupacion,'time':time})


def actualizarempleado(request):
    
    if request.method=='POST':
        id=request.POST['id']
        carnet=request.POST['carnet']
        try:
            myfile = request.FILES['image']
            dir_faces = os.getcwd()
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            
            uploaded_file_url = fs.url(filename)
            
            full_url=dir_faces+"/"+uploaded_file_url[1:]

            path_to_image=full_url
            cascPath=dir_faces+"/"+"haarcascades/haarcascade_frontalface_default.xml"
            original_image = cv2.imread(path_to_image)
            if original_image is not None:
               
                faceCascade=cv2.CascadeClassifier(cascPath)
                gray=cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY)
                faces=faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                if len(faces)==0:
                    os.remove(full_url)
                    return redirect('editarempleado/'+id)
                elif len(faces)>1:
                    os.remove(full_url)
                    return redirect('editarempleado/'+id)
                else:
                    img_width, img_height = 500, 500
                    size = 6
                    pathcore = os.path.join(dir_faces, "CoreDatos")
                    path = os.path.join(pathcore, carnet)
                    if not os.path.isdir(pathcore):
                        os.mkdir(pathcore)
                        
                            # Si no hay una carpeta con el nombre ingresado entonces se crea
                    if not os.path.isdir(path):
                        os.mkdir(path)
                        
                    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
                    faces1 = faceCascade.detectMultiScale(mini)    
                    faces1 = sorted(faces1, key=lambda x: x[3])
                    face_i = faces1[0]
                    (x, y, w, h) = [v * size for v in face_i]
                    face1 = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face1, (img_width, img_height))
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    #Ponemos el nombre en el rectagulo
                    cv2.putText(original_image, carnet, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 255))        
                    #Obtenemos el nombre de la foto
                    #Despues de la ultima sumamos 1 para continuar con los demas nombres
                    pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
                        if n[0]!='.' ]+[0])[-1] + 1        #Metemos la foto en el directorio
                    cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
                    
                    entrenar()
                    nombre=request.POST['nombre']
                    apellido=request.POST['apellido']
                    dept=request.POST['departamento']
                    ocup=request.POST['ocupacion']
                    
                    
                    Empleado.objects.filter(carnet_empleado=carnet).update(foto=filename, nombres=nombre,
                                                                            apellidos=apellido,departamento=dept,ocupacion=ocup)
                    
            
        except:
            nombre=request.POST['nombre']
            apellido=request.POST['apellido']
            dept=request.POST['departamento']
            ocup=request.POST['ocupacion']
            
            
            Empleado.objects.filter(carnet_empleado=carnet).update(nombres=nombre,
                                                                    apellidos=apellido,departamento=dept,ocupacion=ocup)
            
            
             
    return redirect('menu_empleado')

def elegircaramara(request,id):
    contex=Urlcamaraip.objects.filter(es_interna=False)
    return render(request,'empleado/elegircamara/elegircamara.html',{'id':id,'context':contex})

def monitor(request):
    
    return render(request,'empleado/monitor/monitor_captura.html')


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
    time=datetime.now()
    listasincaptura=Empleado.objects.filter(tiene_modelo=0)
    return render(request, 'empleado/listempleado_sin/listasincaptura.html',{'listasincaptura':listasincaptura,'time':time})

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
    