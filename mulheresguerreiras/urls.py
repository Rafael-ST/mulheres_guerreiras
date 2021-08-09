"""mulheresguerreiras URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('sso/', include('sso.urls')),
    path('healthcheck/', lambda r: HttpResponse())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

PROJECT_NAME = 'Mulheres Guerreiras'
admin.site.site_header = "Administração {}".format(PROJECT_NAME)
admin.site.site_title = "{} Portal de Administração".format(PROJECT_NAME)
admin.site.index_title = "Bem vindo ao portal de administração {}".format(PROJECT_NAME)
