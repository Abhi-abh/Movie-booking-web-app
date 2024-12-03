from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('orders/',views.order,name='orders'),
    path('movie_dlt/<int:pk>/',views.movie_dlt,name='movie_dlt'),
    path('booking/',views.booking,name='booking'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('ticket/<int:pk>/',views.ticket,name='ticket'),
    path('payment/',views.payment,name='payment'),
    path('confirmpage/',views.confirmpage,name='confirmpage'),
    path('logout/',views.loggout,name='logout'),

]
