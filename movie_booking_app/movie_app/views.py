from django.shortcuts import render,redirect, get_object_or_404
from .models import Movie,Bookings,Customer,Payment,Contact
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime
import re
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

# Create your views here.

def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password1')
        address=request.POST.get('address')
        phone=request.POST.get('phone')

        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        if not password_pattern.match(password):
            messages.error(request, 'Password must be at least 8 characters long, ''include an uppercase letter, and a special character.')
            return redirect('signup')
        else:

            my_user=User.objects.create_user(uname,email,password)
            my_user.save()
            customer=Customer.objects.create(
                user=my_user,
                phone=phone,
                address=address
            )
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    return render(request,'User/signup.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is incorrect!!!")
            return redirect('login')
    return render(request,'User/login.html')


def home(request):
    movie_list = Movie.objects.order_by('priority')
    movie_dict = {'product':movie_list}
    return render(request,'User/home.html',movie_dict)

def contact(request):
    if request.method == 'POST':
        payment_obj = Contact.objects.create(
            name=request.POST.get('Name'),
            email=request.POST.get('E-mail'),
            description=request.POST.get('Description'),
        )
        if payment_obj:
            payment_obj.save()
            return redirect('contact')
    return render(request,'User/contact.html')

def about(request):
    return render(request,'User/about.html')

@login_required(login_url='login')
def order(request):
    user=request.user
    customer=user.customer_profile
    bookings = Bookings.objects.filter(owner=customer)  # Use select_related for efficiency
    context = {'bookings': bookings}
    return render(request,'User/orders.html',context)

def movie_dlt(request,pk):
    product=Movie.objects.get(pk=pk)
    latest_list = Movie.objects.order_by('-id')[:5]
    context={'product':product,'latest_list':latest_list}
    return render(request,'User/movie_details.html',context)

@login_required(login_url='login')
def booking(request):
    if request.method == 'POST':
        user = request.user
        customer = getattr(user, 'customer_profile', None)  # Safely access customer_profile

        if not customer:
            messages.error(request, "Customer profile not found.")
            return render(request, 'User/booking.html')

        movie_id = request.POST.get('movie_id')  # Get movie_id from the form
        movie = get_object_or_404(Movie, id=movie_id)  # Fetch movie object safely
        seats = request.POST.get('number')

        if not seats or not seats.isdigit():
            messages.error(request, "Invalid number of seats.")
            return render(request, 'User/booking.html')

        seats = int(seats)
        selected_date = request.POST.get('Date')  # Get date from the form
        current_date = now().date()  # Get current date

        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'User/booking.html')

        # Validate selected date
        if selected_date_obj < current_date:
            messages.error(request, "You cannot book for past dates.")
            return render(request, 'User/booking.html')

        # Calculate total price
        total_price = seats * movie.price

        # Create the Booking object without the QR code first
        payment_obj = Bookings.objects.create(
            owner=customer,
            movie=movie,
            date=selected_date,
            seats=seats,
            time=request.POST.get('Time'),
            total_price=total_price,
        )

        # Generate QR code data
        combined_data = (
            f"Movie: {movie.title}\n"
            f"Tickets: {seats}\n"
            f"Date: {selected_date}\n"
            f"Time: {request.POST.get('Time')}\n"
            f"Total: {total_price}"
        )
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data(combined_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code to in-memory buffer
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # Save QR code to the qr_code field
        filename = f"qr_{movie.title[:10]}_{user.id}_{payment_obj.id}.png"
        payment_obj.qr_code.save(filename, ContentFile(buffer.getvalue()))
        payment_obj.save()

        # Redirect to the payment page
        return redirect('payment')

    return render(request, 'User/booking.html')


@login_required(login_url='login')
def payment(request):
    user = request.user
    customer = user.customer_profile
    bookings = Bookings.objects.filter(owner=customer)  # Ensure `bookings` is always initialized

    if request.method == 'POST':
        payment_obj = Payment.objects.create(
            card_name=request.POST.get('name'),
            card_number=request.POST.get('cardNo'),
            month=request.POST.get('month'),
            year=request.POST.get('year'),
            cvv_number=request.POST.get('ccv'),
        )
        # Save the payment object and redirect if successful
        if payment_obj:
            payment_obj.save()
            return redirect('confirmpage')

    return render(request, 'User/payment.html', {'bookings': bookings})


def delete(request,id):
    instance=Bookings.objects.get(pk=id)
    instance.delete()
    if request.method == 'POST':
        return redirect('home')
    dict_insert = {
        'insert' : Bookings.objects.all()
    }
    return render(request,'User/payment.html',dict_insert)

@login_required(login_url='login')
def ticket(request,pk):
    ticket=Bookings.objects.get(pk=pk)
    context={'ticket':ticket}
    return render(request,'User/ticket.html',context)

@login_required(login_url='login')
def confirmpage(request):
    return render(request,'User/confirmationpage.html')

def loggout(request):
    logout(request)
    return redirect('login')