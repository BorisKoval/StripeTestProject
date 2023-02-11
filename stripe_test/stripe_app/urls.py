from django.urls import path

from .views import buy_item
from .views import cancel
from .views import display_item
from .views import success

urlpatterns = [
    path('buy/<int:item_id>', buy_item, name='buy_item'),
    path('item/<int:item_id>', display_item, name='display_item'),
    path('success/', success, name='success'),
    path('cancel/', success, name='cancel'),
]
