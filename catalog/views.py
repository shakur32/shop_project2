from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from decimal import Decimal, InvalidOperation
from .models import Category, Product
from .cart import Cart

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).order_by('-id')[:4]
    return render(request, "catalog/home.html", {"categories": categories, "products": products})

def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=category, is_active=True).prefetch_related('images')

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    else:
        qs = qs.order_by("name")

    paginator = Paginator(qs, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "catalog/product_list.html", {
        "category": category,
        "page_obj": page_obj,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})

# ФУНКЦИИ КОРЗИНЫ
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalog/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('catalog:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('catalog:cart_detail')