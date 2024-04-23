from itertools import product
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import Basket, Product, ProductCategory

# Create your views here.
def index(request):
    context = {
        "title": 'My Store',
    }
    return render(request, 'products/index.html', context=context)

def products(request, category_id=None, page_number=1):
    # if category_id:
    #     category = ProductCategory.objects.get(id=category_id)
    #     products = Product.objects.filter(category=category)
    # else:
    #     products = Product.objects.all()
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    
    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)


    context = {
        'title': 'My Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }
    return render(request=request, template_name='products/products.html', context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
