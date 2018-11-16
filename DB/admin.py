from django.contrib import admin
from .models import Marks
from .models import csvfile

admin.site.register(csvfile)
admin.site.register(Marks)
