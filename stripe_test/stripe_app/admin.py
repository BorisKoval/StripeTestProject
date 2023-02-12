from django.contrib import admin

from .models import Item
from .models import Order

admin.site.register(Item)
admin.site.register(Order)
