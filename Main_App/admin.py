from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Event)
