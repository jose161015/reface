from evento.models import CodigoEvento, Evento
from django.shortcuts import redirect, render,HttpResponse
from empleado.models import Empleado
from datetime import date, datetime, timedelta
from inicio.pdf_utils import render_to_pdf

# Create your views here.
def menu_evento(request):
    return render (request, 'evento/menuevento/menuevento.html')


def regevento(request):
    lempleado=Empleado.objects.all()
    codigoevento=CodigoEvento.objects.all()
    if request.method=='POST':
        empleado=request.POST['empleado']
        cod_evento=request.POST['codevento']
        autorizado=request.POST['aupor']
        descripcion=request.POST['desc']
        fecha1=request.POST['fecha1']
        fecha2=request.POST['fecha2']
        usuario=request.POST['usu_reg']
        now = datetime.now()
        fereg=now.strftime('%Y-%m-%d')
        try:
            Evento.objects.create(
                empleado=Empleado.objects.get(id=empleado),
                codigo_evento=CodigoEvento.objects.get(id=cod_evento),
                justificacion=descripcion,
                autorizado_por=autorizado,
                fecha_inicio=fecha1,
                fecha_fin=fecha2,
                fecha_registro=fereg,
                usuario_registro=usuario
                )
            msgy="Evento guardado exitosamente"
            return render(request,'evento/regevento/regevento.html',{'lempleado':lempleado,'codigoevento':codigoevento,'msgy':msgy})
        except:
            msg="Evento no se guardo correctamente"
        return render(request,'evento/regevento/regevento.html',{'lempleado':lempleado,'codigoevento':codigoevento,'msg':msg})
    return render(request,'evento/regevento/regevento.html',{'lempleado':lempleado,'codigoevento':codigoevento})


def regcodevento(request):
    codevento=CodigoEvento.objects.all()
    if request.method=='POST':
        cod_evento=request.POST['codevento']
        desc=request.POST['desc']
        CodigoEvento.objects.create(cod_evento=cod_evento,descripcion_evento=desc)
    return render (request, 'evento/regcodevento/codevento.html',{'codevento':codevento})
def listarevento(request):
    eve=Evento.objects.all()
    return render(request, 'evento/listarevento/listarevento.html',{'evento':eve,'count':eve.count()})

def editarevento(request,id):
    event=Evento.objects.filter(id=id).first()
    return render(request,'evento/editarevento/editarevento.html',{'event':event,})


def actualizarevento(request):
    if request.method=='POST':
        id=request.POST['id']
        aupor=request.POST['aupor']
        desc=request.POST['desc']
        Evento.objects.filter(id=id).update(autorizado_por=aupor,justificacion=desc)
        return redirect('listarevento')

def eventorango(request):
    if request.method=='GET':
        f1=request.GET['fecha1']
        f2=request.GET['fecha2']
        fecha=datetime.strptime(f2,'%Y-%m-%d')
        nfecha=(fecha+timedelta(days=1))
        fechasumada=nfecha.strftime('%Y-%m-%d')
        registro_rango=Evento.objects.exclude(fecha_inicio__gte=fechasumada).filter(fecha_inicio__gte=f1).order_by('fecha_inicio')
        contenido={'registro_rango':registro_rango,'count':registro_rango.count(),'fecha1':f1,'fecha2':f2}
        return render(request,'eventorango.html',contenido)

def eventorangopdf(request):
    if request.method=='GET':
        f1=request.GET['fecha1']
        f2=request.GET['fecha2']
        fecha=datetime.strptime(f2,'%Y-%m-%d')
        nfecha=(fecha+timedelta(days=1))
        fechasumada=nfecha.strftime('%Y-%m-%d')
        registro_rango=Evento.objects.exclude(fecha_inicio__gte=fechasumada).filter(fecha_inicio__gte=f1).order_by('fecha_inicio')
        contenido={'registro_rango':registro_rango,'count':registro_rango.count(),'fecha1':f1,'fecha2':f2}
        pdf=render_to_pdf('evento/eventorangopdf/eventorangopdf.html',contenido)
    return HttpResponse(pdf,content_type='aplicaction.pdf/pdf')
    