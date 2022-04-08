"""Reface_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from inicio.views import index
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='index', permanent=True)),
    path('index', index, name='index'),
    path('empleado/',include('empleado.urls')),
    path('inicio/',include('inicio.urls')),
    path('evento/',include('evento.urls')),
    path('horarios/',include('horarios.urls')),
    path('marcacion/',include('marcacion.urls')),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)