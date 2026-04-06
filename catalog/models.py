from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Категория")
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = "Категории"
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="Товар")
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток")
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

class Publication(models.Model):
    STATUS_CHOICES = [('draft', 'Черновик'), ('published', 'Опубликовано')]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_description = models.CharField(max_length=500, verbose_name="Описание")
    full_text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to='publications/', blank=True, null=True, verbose_name="Картинка")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    likes = models.ManyToManyField(User, related_name='liked_pubs', blank=True)

    def __str__(self): return self.title
    def get_absolute_url(self):
        return reverse('catalog:publication_detail', kwargs={'pk': self.pk})