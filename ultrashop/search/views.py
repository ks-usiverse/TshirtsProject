from django.shortcuts import render
from store.models import Product
from django.db.models import Q

def searchResult(request):
    if 'kw' in request.GET:
        query = request.GET.get('kw')
        products = Product.objects.all().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )  

    return render(request, 'search.html', {'query':query, 'products':products} )      
