from django.urls import path
from . import views #Importa todas as views que encontrar nessa pasta.

urlpatterns = [
    path('',views.post_list,name='post_list')
]
