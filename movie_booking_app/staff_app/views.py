from django.shortcuts import render,HttpResponse,get_object_or_404
from movie_app.models import Movie,UpcomingMovies,Bookings,Customer,Payment,Contact
from .form import insert_form
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:  # Allow only staff or admin users
                auth_login(request, user)
                return redirect('home1')
            else:
                messages.error(request, "Access restricted to admin or staff users only!")
                return redirect('login1')
        else:
            messages.error(request, "Username or Password is incorrect!")
            return redirect('login1')
    return render(request, 'staff/login.html')


@login_required(login_url='login1')
def home(request):
    movie_list = Movie.objects.order_by('priority')
    movie_dict = {'product':movie_list}
    return render(request,'staff/home.html',movie_dict)


def insert(request):
    if request.method == 'POST':
        form = insert_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            dict_insert = {
        'product' : Movie.objects.all()
    }
        return render(request,'staff/home.html',dict_insert)
        
    form = insert_form()
    dict_form={
        'form':form
    }
    return render(request,'staff/insert.html',dict_form)

@login_required(login_url='login1')
def edit(request,id):
    instance_to_edit=Movie.objects.get(pk=id)
    if request.POST:
        form=insert_form(request.POST,request.FILES,instance=instance_to_edit)
        if form.is_valid():
            instance_to_edit.save()
            dict_insert = {
        'product' : Movie.objects.all()
    }
        return render(request,'staff/home.html',dict_insert)
    else:
        form=insert_form(instance=instance_to_edit)
    return render(request,'staff/edit.html',{'form':form})

@login_required(login_url='login1')
def delete(request,id):
    instance=Movie.objects.get(pk=id)
    instance.delete()
    dict_insert = {
        'product' : Movie.objects.all()
    }
    return render(request,'staff/home.html',dict_insert)

def loggout(request):
    logout(request)
    return redirect('login1')
