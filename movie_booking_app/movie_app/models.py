from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    language = models.CharField(max_length=200,default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    cover_image = models.ImageField(upload_to='covr_image')
    formats = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    certificate = models.CharField(max_length=200)
    year = models.IntegerField()
    cast = models.CharField(max_length=200)
    link = models.URLField()
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile')
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return str(self.user)

class Bookings(models.Model):
    qr_code = models.ImageField(upload_to='qr_codes/',null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True,related_name="bookings")
    total_price = models.FloatField(default=0)
    owner = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='bookings')
    date = models.DateField(null=True, blank=True)
    seats = models.IntegerField()
    time = models.TextField()
    booked_on = models.DateField(auto_now=True)
    
    def __str__(self):
        return "order-{}-{}".format(self.id,self.owner)

class OrededItem(models.Model):
    product = models.ForeignKey(Movie,related_name='added_carts',on_delete=models.SET_NULL,null=True)
    owner = models.ForeignKey(Bookings,on_delete=models.CASCADE,related_name='added_items')

class Payment(models.Model):
    card_name = models.CharField(max_length=250)
    card_number = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100,default=0)
    cvv_number = models.CharField(max_length=100)

    def __str__(self):
        return self.card_name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name