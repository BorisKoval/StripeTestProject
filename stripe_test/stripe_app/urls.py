from django.urls import path

from .views import buy_item
from .views import cancel
from .views import create_order
from .views import display_all_items
from .views import display_item
from .views import pay_order
from .views import success

urlpatterns = [
    path('buy/<int:item_id>', buy_item, name='buy_item'),
    path('item/<int:item_id>', display_item, name='display_item'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('all_items/', display_all_items, name='display_all_items'),
    path('pay/<int:order_id>/<str:session_id>/', pay_order, name='pay_order'),
    path('create_order/<str:item_ids>', create_order, name="create_order"),
]
