from django.urls import path
from . import views

urlpatterns = [
    
    path('home1/',views.home,name='home1'),
    path('login1/',views.login,name='login1'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('insert/',views.insert,name='insert'),
    path('delete1/<int:id>',views.delete,name='delete1'),
]

