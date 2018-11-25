from django.contrib import admin
from .models import Marks
from .models import csvfile
from .models import Enrollments


admin.site.register(csvfile)
admin.site.register(Marks)
admin.site.register(Enrollments)