from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views import View
from .models import Category, Product, Publication
from .forms import PublicationForm

def home(request):
    products = Product.objects.filter(is_active=True).order_by('-id')[:4]
    return render(request, "catalog/home.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})

def cart_detail(request):
    return render(request, "catalog/cart.html")

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
    form_class = PublicationForm
    template_name = 'catalog/publication_form.html'
    permission_required = 'catalog.add_publication'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PublicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'catalog/publication_form.html'
    def test_func(self):
        return self.request.user == self.get_object().author or self.request.user.is_staff

class PublicationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Publication
    template_name = 'catalog/publication_confirm_delete.html'
    success_url = reverse_lazy('catalog:publication_list')
    permission_required = 'catalog.delete_publication'

class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        pub = get_object_or_404(Publication, pk=pk)
        liked = request.user not in pub.likes.all()
        if liked: pub.likes.add(request.user)
        else: pub.likes.remove(request.user)
        return JsonResponse({'liked': liked, 'count': pub.likes.count()})