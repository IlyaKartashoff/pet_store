from django.shortcuts import render

from products.models import Product, ProductCategory

# Create your views here.
def index(request):
    context = {
        "title": 'My Store',
    }
    return render(request, 'products/index.html', context=context)

def products(request):
    context = {
        'title': 'My Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request=request, template_name='products/products.html', context=context)
