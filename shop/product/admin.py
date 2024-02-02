from django.contrib import admin
from .models import Product, ProductImage, Varrient, Comment, Category, Factor, FactorItems, Item,TransferRent


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class VarrientInline(admin.TabularInline):
    model = Varrient


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product',)
    list_filter = ('product', 'user',)


@admin.register(Category)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('category', 'name',)
    list_filter = ('name',)


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'review', 'get_total_like')
    raw_id_fields = ('category',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    inlines = [ProductImageInline, VarrientInline, ]


@admin.register(Varrient)
class VarrientAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_price', 'unit_profit', 'discount', 'quantity',)
    list_filter = ('quantity',)

    def total_price(self, instance):
        return instance.get_total_price()

    def unit_profit(self, instance):
        return instance.get_unit_profit()


class FactorItemsInline(admin.TabularInline):
    model = FactorItems
    readonly_fields = ('factor', 'item_var', 'factory_price', 'unit_price',
                       'total_price', 'discount', 'quantity', 'unit_profit', 'total_profit',)


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    model = Factor
    readonly_fields = ( 'created', 'user', 'payment', 'sum_factory_price', 'sum_unit_price',
                       'sum_total_price', 'sum_total_profit',)
    inlines = [FactorItemsInline, ]


class ItemInline(admin.TabularInline):
    model = Item
    readonly_fields = ('id', 'quantity', 'varrient',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ('id', 'quantity', 'varrient',)
    readonly_fields = ('id', 'quantity', 'varrient',)



@admin.register(TransferRent)
class TransferRentAdmin(admin.ModelAdmin):
    model = TransferRent

