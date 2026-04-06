from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('catalog:product_detail', kwargs={'slug': self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

class Publication(models.Model):
    STATUS_CHOICES = [('draft', 'Черновик'), ('published', 'Опубликовано')]
    title = models.CharField(max_length=200)
    short_description = models.TextField(max_length=500)
    full_text = models.TextField()
    image = models.ImageField(upload_to='publications/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.ManyToManyField(User, related_name='pub_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def get_absolute_url(self): return reverse('catalog:publication_detail', args=[str(self.id)])