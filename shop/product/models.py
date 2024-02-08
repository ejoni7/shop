from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from django.db import models
from accounts.models import User
from django.urls import reverse
from django.db.models import Sum


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

    def clean(self):
        if self.get_total_price() - self.product.factory_price <= 5000:
            raise ValidationError("حاشیه سود بسیار پایین است")


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
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_factors')
    payment = models.PositiveIntegerField()
    sum_factory_price = models.PositiveIntegerField(default=0)
    sum_unit_price = models.PositiveIntegerField(default=0)
    sum_total_price = models.PositiveIntegerField(default=0)
    sum_total_profit = models.PositiveIntegerField(default=0)
    transfer = models.PositiveIntegerField(default=0)
    created = jmodels.jDateTimeField(auto_now_add=True)

    def month_with_sum(self):
        data = list()
        first = Factor.objects.first()
        last = Factor.objects.last()
        month_ = first.created.month
        year_ = first.created.year
        sum_total = 0
        suman = 0
        for object in Factor.objects.all().order_by('created'):
            object_year = object.created.year
            object_month = object.created.month

            def end():
                if object.id == last.id:
                    time = f'{month_}/{year_}'
                    data.append((time, suman, sum_total))

            if object_month != month_ or object_year != year_:
                time = f'{month_}/{year_}'
                data.append((time, suman, sum_total))
                suman = object.sum_total_profit
                sum_total = object.sum_total_price
                month_ = object_month
                year_ = object_year
                end()
            else:
                suman += object.sum_total_profit
                sum_total += object.sum_total_price
                end()

        return data

    # def monthly_profit_list(self):
    #     first_object = Factor.objects.first().created
    #     last_object = Factor.objects.last().created
    #     self.f_month = int(first_object.month)
    #     self.f_year = int(first_object.year)
    #     self.l_month = int(last_object.month)
    #     self.l_year = int(last_object.year)
    #     tot_sum = list()
    #     def add_sum(month, year):
    #         suman = Factor.objects.filter(created__year=year,created__month=month).aggregate(Sum('sum_total_profit'))
    #         print(suman)
    #         tot_sum.append(suman)
    #         if month < 12:
    #             month += 1
    #         else:
    #             month = 1
    #             year += 1
    #         if year < self.l_year or month <= self.l_month:
    #             add_sum(month, year)
    #         else:
    #             return tot_sum
    #     add_sum(self.f_month, self.f_year)

    def __str__(self):
        return self.user.username
    # def get_total_profit_of_month(self):
    #     month = self.created.month
    #     year = self.created.year
    #     self.profit_of_month = 0
    #     for object in Factor.objects.all():
    #         if object.created.month == month and object.created.year == year:
    #             self.profit_of_month += object.sum_total_profit
    #     return self.profit_of_month


class FactorItems(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='factor_items')
    item_name = models.CharField(max_length=150)
    factory_price = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    unit_profit = models.PositiveIntegerField()
    total_profit = models.PositiveIntegerField()

    def __str__(self):
        return self.item_name
