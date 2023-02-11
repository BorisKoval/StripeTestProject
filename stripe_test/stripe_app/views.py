import stripe
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render

from django.conf import settings
from django.urls import reverse

from .models import Item, Order


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


def display_all_items(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'all_items.html', context)


def pay_order(request, order_id, session_id):

    order = Order.objects.get(id=order_id)
    session = stripe.checkout.Session.retrieve(session_id)
    context = {
        "order": order,
        "session": session,
        'stripe_public_key': settings.STRIPE_PUBLIC_API_KEY
    }
    return render(request, "pay_order.html", context)


def create_order(request, item_ids):
    items = Item.objects.filter(id__in=item_ids)
    total_cost = sum([item.price for item in items])
    order = Order.objects.create(total_cost=total_cost)
    order.items.set(items)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.name,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": 1,
            }
            for item in items
        ],
        mode="payment",
        # success_url=request.build_absolute_uri(reverse("success")),
        # cancel_url=request.build_absolute_uri(reverse("cancel")),
        success_url=f"http://{request.META['HTTP_HOST']}/stripe/success/",
        cancel_url=f"http://{request.META['HTTP_HOST']}/stripe/cancel/",
    )

    return redirect(f"/pay/{order.id}/{session.id}")
