from django.contrib import admin
from . models import Movie,Bookings,Payment,Contact

# Register your models here.

admin.site.register(Movie)
admin.site.register(Bookings)
admin.site.register(Payment)
admin.site.register(Contact)