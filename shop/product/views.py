from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Varrient, Item, Product, Comment, FactorItems, Factor, TransferRent
from .forms import CommentForm, SendInfoForm
from django.contrib import messages
from accounts.models import User


# Create your views here.

def pagination(page__, quantity, instances, ordering, radius):
    p = Paginator(instances.order_by(ordering), quantity)
    page_ = p.page(int(page__))
    return {'queries': page_, 'page': p, 'page_num': page__, 'radius': radius}


def home(request, page=1):
    if request.method == 'POST':
        return HttpResponse('im in product home')
    else:
        products = Product.objects.all()
        context = pagination(page, 4, products, '-created', 2)
        return render(request, 'product/home.html', context)


def product(request, slug, id):
    product = get_object_or_404(Product, slug__exact=slug, id=id)
    form = CommentForm()
    related_products = Product.objects.filter(category_id=product.category.id).exclude(id=id)[:5]
    select = product.product_varrients.all()[0].id
    if request.method == 'POST':
        select = int(request.POST.get('select'))
    else:
        product.review += 1
        product.save()

    return render(request, 'product/product.html',
                  {'product': product, 'related_products': related_products, 'form': form, 'select': select, })


#                                 needs javascript to just call the function with out  out put
@login_required(login_url='accounts:login')
def send_comment(request):
    refer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user_id=request.user.id, product_id=id, text=form.cleaned_data['text'])
            messages.success(request, "کامنت شما ایجاد شد")
            return redirect(refer)


#                                 needs javascript to just call the function and send message with json
@login_required(login_url='accounts:login')
def product_like(request, id):
    refer = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    if request.user not in product.like.all():
        product.like.add(request.user)
    message = 'user liked'
    return redirect(refer)


@login_required(login_url='accounts:login')
def card(request):
    if request.method == 'POST':
        form = SendInfoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        user = request.user
        user.address = data['address']
        user.save()
        messages.success(request, 'ادرس با موفقیت ویرایش شد')
        return redirect('product:card')
    else:
        check_quantity(request.user.id)
        rent = TransferRent.objects.latest('rent').rent
        return render(request, 'product/card.html', {'rent': rent, 'sum': sum(request.user.id)})


def check_quantity(id):
    user = User.objects.get(id=id)
    for item in user.user_items.all():
        quant = item.varrient.quantity
        if item.quantity > quant:
            if quant != 0:
                item.quantity = item.varrient.quantity
                item.save()
            else:
                item.delete()


def sum(id):
    sum = 0
    for item in User.objects.get(id=id).user_items.all():
        sum += item.quantity * item.varrient.get_total_price()
    return sum


#                                 needs javascript to just call the function and return quantity at 115,118
#                                 and maybe remove succes message at 117
@login_required(login_url='accounts:login')
def add_item_to_card(request, id):
    refer = request.META.get('HTTP_REFERER')
    quant = request.POST.get('quantity') or 1
    quant = int(quant)
    for item in request.user.user_items.all():
        if item.varrient.id == id:
            if item.varrient.quantity >= quant and quant > 0:
                item.quantity = quant
                item.save()
                return redirect(refer)
    item = Item.objects.create(quantity=quant, varrient_id=id, user_id=request.user.id)
    messages.success(request, 'ایتم اضافه شد')
    return redirect(refer)


#                                 needs javascript to just call the function with out  out put
@login_required(login_url='accounts:login')
def delete_item(request, id):
    refer = request.META.get('HTTP_REFERER')
    item = get_object_or_404(Item, id=id)
    item.delete()
    return redirect(refer)


#                                 needs javascript to just call the function and return message
#                                 if item exist return the item.quantity
#                                        else return None
@login_required(login_url='accounts:login')
def mines_of_card(request, id):
    refer = request.META.get('HTTP_REFERER')
    item = get_object_or_404(Item, id=id)
    item.quantity -= 1
    item.save()
    message = item.quantity
    if item.quantity <= 0:
        item.delete()
        message = 'None'
    return redirect(refer)


#                                 needs javascript to just call the function and return message

@login_required(login_url='accounts:login')
def add_to_card(request, id):
    refer = request.META.get('HTTP_REFERER')
    item = get_object_or_404(Item, id=id)
    if item.quantity < item.varrient.quantity:
        item.quantity += 1
        item.save()
    message = item.quantity
    return redirect(refer)


def after_buy(user_id, payment):
    user = User.objects.get(id=user_id)
    if user.user_items.all():

        factor = Factor.objects.create(user_id=user_id, payment=payment)
        factor.transfer = TransferRent.objects.latest('rent').rent
        for item in user.user_items.all():
            var = item.varrient
            factory_price = var.product.factory_price
            unit_price = var.unit_price
            total_price = var.get_total_price()
            unit_profit = total_price - factory_price
            quantity = item.quantity
            total_profit = quantity * unit_profit
            factor.sum_factory_price += factory_price * quantity
            factor.sum_unit_price += unit_price * quantity
            factor.sum_total_price += total_price * quantity
            factor.sum_total_profit += total_profit
            factor.save()
            FactorItems.objects.create(factor_id=factor.id,
                                       item_name=f"  محصول {item.varrient.product.name} تنوع {item.varrient.name}  کد تنوع   {item.varrient.id}   ",
                                       factory_price=factory_price,
                                       unit_price=unit_price,
                                       total_price=total_price,
                                       discount=var.discount,
                                       quantity=quantity,
                                       unit_profit=unit_profit,
                                       total_profit=total_profit, )
        for item in user.user_items.all():
            item.varrient.quantity -= item.quantity
            item.varrient.save()
            item.delete()


@login_required(login_url='accounts:login')
def pay(request):
    if request.method=='POST':
        payment_ = 15060000
        user_id = request.user.id
        after_buy(user_id, payment_)
        return redirect('product:card')
