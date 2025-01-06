from django.contrib import admin
from . models import Movie,Bookings,Payment,Contact,UpcomingMovies,Customer

# Register your models here.

admin.site.register(Movie)
admin.site.register(UpcomingMovies)
admin.site.register(Bookings)
admin.site.register(Contact)
class user(admin.ModelAdmin):
    list_display = ('name','address','phone')
admin.site.register(Customer,user)