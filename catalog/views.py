from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views import View

# Модели
from django.contrib.auth.models import User
from .models import Product, Publication, Task

# Инструменты для API (DRF)
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import TaskSerializer, UserSerializer

import logging

# Настройка логирования
logger = logging.getLogger('catalog')

# =========================================================
# 1. REST API (Тема 10-11)
# =========================================================

class UserCreateView(viewsets.ModelViewSet):
    """Регистрация новых пользователей через API"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    """Управление задачами через API"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'priority']

    def get_queryset(self):
        # Оптимизация: загружаем владельца сразу и фильтруем только свои задачи
        return Task.objects.filter(owner=self.request.user).select_related('owner')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        logger.info(f"API: Пользователь {self.request.user.username} создал задачу.")

    def perform_destroy(self, instance):
        logger.warning(f"API: Пользователь {self.request.user.username} удалил задачу {instance.id}.")
        instance.delete()

# =========================================================
# 2. МАГАЗИН (Твои iPhone и корзина)
# =========================================================

def home(request):
    """Главная страница со списком товаров"""
    products = Product.objects.filter(is_active=True).order_by('-id')
    return render(request, "catalog/home.html", {"products": products})

def product_detail(request, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})

def cart_detail(request):
    """Просмотр корзины"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * item['quantity']
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total
            })
        except (Product.DoesNotExist, ValueError):
            continue
    
    return render(request, "catalog/cart_detail.html", {
        'cart_items': cart_items,
        'total_price': total_price
    })

def add_to_cart(request, product_id):
    """Добавление в корзину"""
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    if p_id in cart:
        cart[p_id]['quantity'] += 1
    else:
        cart[p_id] = {'quantity': 1}
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('catalog:cart_detail')

def clear_cart(request):
    """Очистка корзины"""
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('catalog:cart_detail')

# =========================================================
# 3. БЛОГ (Публикации)
# =========================================================

class PublicationListView(ListView):
    model = Publication
    template_name = 'catalog/publication_list.html'
    context_object_name = 'publications'
    def get_queryset(self):
        return Publication.objects.filter(status='published').order_by('-created_at')

class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'catalog/publication_detail.html'

class PublicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Publication
    fields = ['title', 'short_description', 'full_text', 'image', 'status']
    template_name = 'catalog/publication_form.html'
    permission_required = 'catalog.add_publication'
    success_url = reverse_lazy('catalog:publication_list')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PublicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Publication
    fields = ['title', 'short_description', 'full_text', 'image', 'status']
    template_name = 'catalog/publication_form.html'
    success_url = reverse_lazy('catalog:publication_list')
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.is_staff

class PublicationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Publication
    template_name = 'catalog/publication_list.html' 
    success_url = reverse_lazy('catalog:publication_list')
    permission_required = 'catalog.delete_publication'

class AddLikeView(LoginRequiredMixin, View):
    """Лайки для статей"""
    def post(self, request, pk):
        pub = get_object_or_404(Publication, pk=pk)
        if request.user in pub.likes.all():
            pub.likes.remove(request.user)
            liked = False
        else:
            pub.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'count': pub.likes.count()})