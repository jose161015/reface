from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from marcacion.models import Urlcamaraip

# Create your views here.
def index(request):
    contex=Urlcamaraip.objects.filter(es_interna=False)
    
    return render(request,'inicio/index/index.html',{'context':contex})


def login_view(request):
	if request.method=='POST':
		username=request.POST['usuario']
		password=request.POST['pass']
		user=authenticate(request, username=username,password=password)
		if user is not None:
			login(request,user)
			if user.is_superuser:
				return redirect('/admin/')
			else:
				return redirect('menu')
		else:
			return render(request, 'login/login.html',{'error':'Usuario o contraseña invalido'})
	return render(request, 'login/login.html')


def menu_view(request):
    return render(request,'inicio/menu/menu.html')

def logout_view(request):
    logout(request)
    return redirect('index')