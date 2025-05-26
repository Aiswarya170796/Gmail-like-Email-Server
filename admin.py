from django.contrib import admin

# Register your models here.
from .models import Email,Recipient
admin.site.register(Email)
admin.site.register(Recipient)