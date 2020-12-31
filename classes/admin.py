from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Contact)
admin.site.register(teacher)

admin.site.register(testinomial)
admin.site.register(resultslider)
admin.site.register(Student)