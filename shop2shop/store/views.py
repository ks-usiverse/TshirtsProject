from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from .process_cookie import *


def store(request):
    Data = cart_data(request)
    cartItems = Data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/store.html', context)


def cart(request):
    Data = cart_data(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)


def checkout(request):
    Data = cart_data(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/payment.html', context)


def updatedItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('Product:', productID)
    print('Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):
    # print("Data:" , request.body)
    transation_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)



    else:
        customer, order = customer_order(request, data)

    total = float(data['form']['total'])
    order.transation_id = transation_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAdress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],

        )

    return JsonResponse('Payment Completed!', safe=False)