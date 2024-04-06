from django.contrib import admin

# Register your models here.

from  .models import Service, Monitor_Log

admin.site.register(Service)
admin.site.register(Monitor_Log)