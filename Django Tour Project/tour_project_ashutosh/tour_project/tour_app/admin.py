from django.contrib import admin

# Register your models here.
from .models import packages,user_booking,Places
# Register your models here.
admin.site.register(packages)
admin.site.register(user_booking)
admin.site.register(Places)
# admin.site.register(search)