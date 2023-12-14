"""
URL configuration for firebase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),
    path('postsign/', views.postsign),
    path('postsignup/', views.postsignup),
    path('filupload/', views.upload_file),
    path('myuploads/', views.display_items),
    path('home/', views.home),
    path('updateProfile/', views.update_profile),
    path('viewProfile/', views.view_profile),
    path('user_details/', views.user_details),

    path('logout/', views.logout),
    # path('download/', views.download),
    path('test/', views.test),
    path('deleteUser/', views.deleteUser),


]
