from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("URL (slug)", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("URL (slug)", unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    old_price = models.DecimalField("Старая цена", max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField("Описание", blank=True)
    stock = models.PositiveIntegerField("В наличии", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("Изображение", upload_to='products/')
    alt_text = models.CharField("Текст вместо фото", max_length=200, blank=True)
    is_main = models.BooleanField("Главное фото", default=False)