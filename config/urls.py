"""
URL configuration for config project.

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

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.contrib import admin
from django.urls import path
from myprojectapp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]

from django.urls import path
from myprojectapp.views import get_data

urlpatterns = [
    path('api/data/', get_data),
]

from django.contrib import admin
from django.urls import path
from myprojectapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home),

    path('preorder/', views.preorder),
    path('preorderaction/', views.preorderaction),
    path('preorders/', views.preorders),

    path('admin_dashboard/', views.admin_dashboard),
    path('worker/',views.worker),
    path('assign_worker/', views.assign_woker),
    path('assign_workeraction/', views.assign_workeraction),
     path('workers/', views.worker),
      path(
        'workers/<int:id>/',
        views.workers
    ),
    path('assign_order/',views.assign_order),
    path('assign_order/<int:customer_id>/<int:worker_id>/',views.assign_order,name='assign_order'),
    path('selectwoker/',views.assign),
    path(
    'selectworker/<int:id>/',
    views.assign),
   # path('select_worker/<int:id>/', views.select_worker),
    path('select_worker/<int:id>/', views.select_worker, name='select_worker'),
    path('home/',views.loginaction),
    path('worker_dashboard/',views.worker_dashboard),
    path('loginaction/',views.loginaction,name='loginaction'),
    path('neworders/',views.neworders,name='neworders'),
    path('accept_order/<int:id>/', views.accept_order),
    path('completed_order/<int:id>/', views.completed_order),
    path('completedorders/',views.completedorders),
    path('trackorder/',views.trackorder,name='trackorder'),
    path('worker_order/<int:worker_id>/',views.worker_order,name='worker_order'),
    path('current_order/<int:id>/',views.current_order,name='current_order'),
    path('completed_order/<int:id>/',views.completed_order,name='completed_order'),
    path('completed_ordert/<int:id>/',views.completed_ordert,name='completed_ordert'),
    path('editworker/<int:id>/', views.editworker, name='editworker'),
    path('update_worker/<int:id>/', views.update_worker,name='update_worker'),
    path('delete_worker/<int:id>/', views.delete_worker,name='delete_worker'),

]