from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from .models import *
import json
import datetime
from . cookie_handling import *
from django.views.generic import CreateView, DetailView,TemplateView,View
from django.contrib.auth.forms import UserCreationForm
from .forms import ProductForm,CreateUserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages




class StoreView(TemplateView):
    template_name = "store/store.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Data = cart_data(self.request)
        cartItems = Data['cartItems']
        products = Product.objects.all()
        context['products'] = products
        context['cartItems'] = cartItems
        return context



def store(request):
    Data = cart_data(request)
    cartItems = Data['cartItems']

    products = Product.objects.all()
    context = {'products':products,'cartItems': cartItems }

    return render(request, 'store/store.html', context)

class CartView(TemplateView):
    template_name = "store/cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Data = cart_data(self.request)
        cartItems = Data['cartItems']
        order = Data['order']
        items = Data['items']
        context['items'] = items
        context['order'] = order
        context['cartItems'] = cartItems
        return context



def cart(request):
    Data = cart_data(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items'] 

    context = {'items': items, 'order':order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)

class CheckoutView(TemplateView):
    template_name = "store/payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Data = cart_data(self.request)
        cartItems = Data['cartItems']
        order = Data['order']
        items = Data['items']
        context['items'] = items
        context['order'] = order
        context['cartItems'] = cartItems
        return context


def checkout(request):
    
    Data = cart_data(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']  

    context = {'items': items, 'order':order,'cartItems': cartItems}

    return render(request, 'store/payment.html', context)

class UpdatedItemView(View):
    def post(self, request, *args, **kwargs):
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



        return JsonResponse('Item added', safe =False)


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



        return JsonResponse('Item added', safe =False)    



@csrf_exempt


def processOrder(request):
    #print("Data:" , request.body)
    transation_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        

    else:
        customer,order = customer_order(request,data)
        

    total = float(data['form']['total'])
    order.transation_id = transation_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    
    if order.shipping == True:
        ShippingAdress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],



        )            


    return JsonResponse('Payment Completed!', safe =False) 


class RegistrationView(CreateView):
    template_name = "store/registration.html"
    #form_class = UserCreationForm
    form_class = CreateUserForm
    success_url = "/"

class ProductDetailView(DetailView):
    template_name = "store/product_detail.html"
    queryset = Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Data = cart_data(self.request)
        cartItems = Data['cartItems']
        context['cartItems'] = cartItems
        return context



class ProductAddView(CreateView):
    form_class = ProductForm
    template_name = "store/add_product.html"
    success_url = "/"

# def add_comment(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.product = product
#             comment.save()
#             return redirect('product_detail', pk=product.pk)
#     else:
#         form = CommentForm()
#
#     return render(request, 'store/add_comment.html', {'form': form})
#
#
# @login_required
# def comment_modify(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#
#     if request.method == "POST":
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             comment = form.save()
#             comment.modify_date = timezone.now()
#             comment.save()
#             return redirect('product_detail', pk=comment.product.pk)
#     else:
#         form = CommentForm(instance=comment)
#     return render(request, 'store/add_comment.html', {'form': form})
#
#
#
#
# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.delete()
#     return redirect('product_detail', pk=comment.product.pk)





