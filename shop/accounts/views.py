from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import ContextMixin

from .form import *
from django.utils.crypto import get_random_string
from .models import User
from django.contrib.auth import authenticate, logout, REDIRECT_FIELD_NAME
from django.contrib.auth import login as login_
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
# from kavenegar import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from sorl.thumbnail import get_thumbnail
from django.contrib.auth import authenticate


# Create your views here.
class Rules(generic.TemplateView):
    template_name = 'accounts/rules.html'



# def send_sms(request, number, template, message):
#     try:
#         api = KavenegarAPI(
#             '66794E75437974365963452B2F367331586E656E6A37722F4F6F5550584E534F4A48556E6B4D725238334D3D')
#         params = {
#             'receptor': number,
#             'template': template,
#             'token': message,
#             'type': 'sms',  # sms vs call
#         }
#         response = api.verify_lookup(params)
#         print(response)
#     except APIException as e:
#         print(e)
#     except HTTPException as e:
#         print(e)


def login(request):
    if request.user.is_authenticated:
        return redirect('product:home')
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form, })
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, phone=User.objects.get(username=data['phone']).phone,
                                    password=data['password'])
            except:
                user = authenticate(request, phone=data['phone'], password=data['password'])

            if user:
                login_(request, user)
                return redirect('product:home')
            else:
                messages.warning(request, 'کاربری با مشخصات وارد شده یافت نشد')
                return redirect('accounts:login')
        else:
            messages.warning(request, 'اطلاعات وارد شده صحیح نیست')
            return redirect('accounts:login')



def register(request):
    if request.user.is_authenticated:
        return redirect('product:home')
    global random_code, number, reguser
    random_code = randint(1000, 9999)
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form, })
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            number = data['phone']
            reguser = User.objects.create_user(username=data['username'], phone=number,
                                               password=data['password_2'], )

            messages.success(request, ' برای وارد شدن  لطفا پیامک ارسال شده را برای ما ارسال کنید!')
            send_sms(request, (number,), 'verify', random_code)
            return redirect('accounts:phone_check')
        else:
            messages.warning(request, 'اطلاعات وارد شده صحیح نمیباشند')
            return redirect('accounts:register')


def logout_(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user, )
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'پروفایل با موفقیت ویرایش شد', 'success')
        else:
            messages.warning(request, 'اطلاعات وارد شده صحیح نیست!', 'warning')
        return redirect('accounts:profile')

    else:
        user_form = UserForm(instance=request.user)
        return render(request, 'accounts/profile.html',
                      {'user_form': user_form, })


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(request.user, request.POST)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'پسورد با موفقیت نغییر کرد ')
        else:
            messages.warning(request, 'تغیرات پسورد ناموفق ')
        return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password_check.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = get_object_or_404(User, phone__exact=data['number'], username__exact=data['username'])
            randomical_password = get_random_string(length=10)
            user.set_password(randomical_password)
            user.save()
            # sms nem password for him
            messages.success(request, 'پسورد جدید برای شما پیامک شد')
            return redirect('accounts:login')
        else:
            messages.warning(request, 'شماره همراه یا نام کاربری نامعتبر است')
            return redirect('accounts:register')
    else:
        form = ForgetPasswordForm()
        return render(request, 'accounts/forget_password.html', {'form': form})


def phone_check(request):
    if request.method == 'GET':
        form = CodeForm()
        return render(request, 'accounts/phone_check.html', {'form': form})
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['code'] == random_code:
                reguser.save()
                messages.success(request, 'حساب کاربری برای شما فعال شد')
                return redirect('accounts:login')
            else:
                messages.warning(request, 'اطلاعات وارد شده صحیح نیست')
                return redirect('accounts:phone_check')

# class ForgetPassword(auth_views.PasswordResetView):
#     template_name = 'accounts/reset_password.html'
#     success_url = reverse_lazy('accounts:password_reset_done')
#     email_template_name = 'accounts/link.html'
#
#
# class ResetDone(auth_views.PasswordResetDoneView):
#     template_name = 'accounts/reset_password_done.html'
#
#
# class ConfirmPassword(auth_views.PasswordResetConfirmView):
#     template_name = 'accounts/confirm_password.html'
#     success_url = reverse_lazy('accounts:confirm_done')
#
#
# class ConfirmDone(auth_views.PasswordResetCompleteView):
#     template_name = 'accounts/confirm_done.html'
