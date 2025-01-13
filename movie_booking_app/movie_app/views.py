from django.shortcuts import render,redirect, get_object_or_404
from .models import Movie,UpcomingMovies,Bookings,Customer,Payment,Contact
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime,date
import re
import qrcode
from io import BytesIO
from calendar import monthrange
from django.core.files.base import ContentFile
from django.db.models import Sum
from django.utils import timezone

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
                name=uname,
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
    up_movies = UpcomingMovies.objects.all()
    movie_dict = {'product':movie_list,'upmovies':up_movies}
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
            messages.success(request, 'Form Successfully Submitted')
            return redirect('contact')
            
    return render(request,'User/contact.html')

def about(request):
    return render(request,'User/about.html')

@login_required(login_url='login')
def order(request):
    user=request.user
    customer=user.customer_profile
    bookings = Payment.objects.filter(owner=customer)   # Use select_related for efficiency
    context = {'bookings': bookings}
    return render(request,'User/orders.html',context)

def movie_dlt(request, pk):
    product = Movie.objects.get(pk=pk)
    latest_list = Movie.objects.order_by('-id')[:5]
    today = date.today()
    current_date = now().date()
    current_time = timezone.localtime(timezone.now()).time()
    current_year = today.year
    min_date = today.strftime("%Y-%m-%d")
    max_date = date(today.year, today.month, monthrange(today.year, today.month)[1]).strftime("%Y-%m-%d")

    if request.method == 'POST':
        user = request.user
        customer = getattr(user, 'customer_profile', None)  # Safely access customer_profile

        if not customer:
            messages.error(request, "Customer profile not found.")
            return redirect('movie_dlt', pk=pk)

        movie_id = request.POST.get('movie_id')  # Get movie_id from the form
        movie = get_object_or_404(Movie, id=movie_id)  # Fetch movie object safely
        seats = request.POST.get('number')

        if not seats or not seats.isdigit():
            messages.error(request, "Invalid number of seats.")
            return redirect('movie_dlt', pk=pk)

        seats = int(seats)
        if seats <= 0:
            messages.error(request, "Number of seats must be greater than zero.")
            return redirect('movie_dlt', pk=pk)

        selected_date = request.POST.get('Date')  # Get date from the form
        selected_time = request.POST.get('Time')  # Get time from the form
        current_date = now().date()  # Get current date
        selected_time_obj = datetime.strptime(selected_time, '%I-%M %p').time()
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()


        if not selected_time:
            messages.error(request, "Please select a valid time.")
            return redirect('movie_dlt', pk=pk)


        if selected_date_obj == current_date:
            if selected_time_obj <= current_time:
                messages.error(request, "The booking is closed for the selected time.")
                return redirect('movie_dlt', pk=pk)

        # Check total seats booked for the selected movie, date, and time
        total_booked_seats = (
            Bookings.objects.filter(movie=movie, date=selected_date_obj, time=selected_time)
            .aggregate(total=Sum('seats'))['total'] or 0
        )
        remaining_seats = 100 - total_booked_seats

        if remaining_seats <= 0:
            messages.error(request, "Tickets are not available for this time slot.")
            return redirect('movie_dlt', pk=pk)

        if seats > remaining_seats:
            messages.error(request, f"Only {remaining_seats} seats are available for this time slot.")
            return redirect('movie_dlt', pk=pk)

        # Calculate total price
        total_price = seats * movie.price

        # Create the Booking object without the QR code first
        payment_obj = Bookings.objects.create(
            owner=customer,
            movie=movie,
            date=selected_date_obj,
            seats=seats,
            time=selected_time,
            total_price=total_price,
        )

        # Generate QR code data
        combined_data = (
            f"Movie: {movie.title}\n"
            f"Tickets: {seats}\n"
            f"Date: {selected_date}\n"
            f"Time: {selected_time}\n"
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

    context = {
        'product': product,
        'latest_list': latest_list,
        'today': date.today().isoformat(),
        'current_year': current_year,
        'min_date': min_date,
        'max_date': max_date,
    }
    return render(request, 'User/movie_details.html', context)


@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    return render(request, 'User/profile.html', {'user': user})

@login_required(login_url='login')
def payment(request):
    # Initialize `bookings` as an empty QuerySet or `None` to handle both POST and GET requests
    bookings = None

    if request.method == 'POST':
        user = request.user
        customer = getattr(user, 'customer_profile', None)  # Ensure the user has a customer profile
        bookings = Bookings.objects.filter(owner=customer)  # Fetch bookings for the customer
        
        booking_id = request.POST.get('booking_id')  # Get movie_id from the form
        movie = get_object_or_404(Bookings, id=booking_id)  # Ensure the booking exists
        
        # Create a new Payment object
        payment_obj = Payment.objects.create(
            card_name=request.POST.get('name'),
            card_number=request.POST.get('cardNo'),
            month=request.POST.get('month'),
            year=request.POST.get('year'),
            cvv_number=request.POST.get('ccv'),
            booking=movie,
            owner = customer , # Associate the payment with the booking
        )

        # Save the payment object and redirect if successful
        if payment_obj:
            payment_obj.save()
            return redirect('confirmpage')  # Redirect to confirmation page

    # Handle GET request or fallback
    else:
        user = request.user
        customer = getattr(user, 'customer_profile', None)  # Ensure the user has a customer profile
        bookings = Bookings.objects.filter(owner=customer) if customer else None  # Fetch bookings if customer exists

    return render(request, 'User/payment.html', {'bookings': bookings})


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