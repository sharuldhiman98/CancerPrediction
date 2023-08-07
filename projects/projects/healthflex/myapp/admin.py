

# Register your models here.
from django.contrib import admin
from myapp.models import Person
admin.site.register(Person) 

from myapp.models import doctor
admin.site.register(doctor) 

from myapp.models import hospital
admin.site.register(hospital) 

from myapp.models import medicine
admin.site.register(medicine) 