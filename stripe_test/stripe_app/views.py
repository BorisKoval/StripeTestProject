import stripe
from django.shortcuts import HttpResponse
from django.shortcuts import render

from django.conf import settings
from .models import Item


def buy_item(request, item_id):

    item = Item.objects.get(pk=item_id)

    price = stripe.Price.create(
        unit_amount=int(item.price * 100),
        currency='usd',
        product=item.product_id,
        nickname=item.name,
    )

    session = stripe.checkout.Session.create(
        api_key=stripe.api_key,
        payment_method_types=['card'],
        line_items=[{
            'price': price.id,
            'quantity': 1,
        }],
        mode="payment",
        success_url=f"http://{request.META['HTTP_HOST']}/stripe/success/",
        cancel_url=f"http://{request.META['HTTP_HOST']}/stripe/cancel/",
    )

    return HttpResponse(session.id)


def display_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(
        request, 'item.html',
        {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_API_KEY}
    )


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
