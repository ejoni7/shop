from django_jalali.db import models as jmodels
from django.db import models
from accounts.models import User
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='related_categories')
    name = models.CharField(max_length=30, )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=70)
    created = jmodels.jDateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="related_products")
    review = models.PositiveIntegerField(default=0)
    slug = models.SlugField(allow_unicode=True, unique=True)
    factory_price = models.IntegerField()
    information = models.TextField(max_length=1000)
    like = models.ManyToManyField(User, related_name='related_like', blank=True)

    def __str__(self):
        return self.name

    @property
    def get_total_like(self):
        return self.like.count()

    def get_absolute_url(self):
        return reverse('product:product', args=[self.slug, self.id])


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    text = models.TextField(max_length=300)


class Varrient(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_varrients')
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_total_price(self):
        self.get_total_price = self.unit_price * (100 - self.discount) / 100
        return int(self.get_total_price)

    def get_unit_profit(self):
        self.get_unit_profit = self.get_total_price - self.product.factory_price
        return self.get_unit_profit


class Item(models.Model):
    quantity = models.PositiveIntegerField()
    varrient = models.ForeignKey(Varrient, on_delete=models.CASCADE, related_name='varrient_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_items')

    def __str__(self):
        return self.varrient.product.name


class TransferRent(models.Model):
    rent = models.PositiveIntegerField()
    def __str__(self):
        return str(self.rent)


class Factor(models.Model):
    created = jmodels.jDateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_factors')
    payment = models.PositiveIntegerField()
    sum_factory_price = models.PositiveIntegerField(blank=True, null=True)
    sum_unit_price = models.PositiveIntegerField(blank=True, null=True)
    sum_total_price = models.PositiveIntegerField(blank=True, null=True)
    sum_total_profit = models.PositiveIntegerField(blank=True, null=True)


class FactorItems(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='factor_items')
    item_var = models.ForeignKey(Varrient, on_delete=models.PROTECT)
    factory_price = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    unit_profit = models.PositiveIntegerField()
    total_profit = models.PositiveIntegerField()
