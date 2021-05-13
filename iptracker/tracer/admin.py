from re import I
from django.contrib import admin
from .models import IpRecord, Country
# Register your models here.

admin.site.register(IpRecord)
admin.site.register(Country)
