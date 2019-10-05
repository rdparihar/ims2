"""prj_bms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .routers import router
from django.views.generic import TemplateView
# from django.contrib.auth import views
from django.contrib.auth import views as auth_views

from django.conf.urls import url





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bms.urls')),
   

    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls'), name='account'),
    # path('login/', include('django.contrib.auth.urls'), name='login'),
    # path('logout/', include('django.contrib.auth.urls'), {'template_name': 'logged_out.html'}, name='logout'),
    # path('logout/', login_views,   name='logout'),
    path ('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path ('accounts/logout/', auth_views.LogoutView.as_view(), name="logout")

]
