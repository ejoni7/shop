from django import forms
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm

errors = {
    'required': 'لطفا فیلد مقابل را پر کنید',
    'invalid': 'فرمت ایمیل وارد شده صحیح نیست'
}


class UserCreatForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'phone', ]

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data['password1']
        password2 = data['password2']
        if password1 and password2 and password2 != password1:
            raise forms.ValidationError('پسوردها با هم متفاوتند')
        return password2


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, error_messages=errors,
                               widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    phone = forms.IntegerField(error_messages=errors)
    password_1 = forms.CharField(max_length=20, error_messages=errors,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسورد'}))
    password_2 = forms.CharField(max_length=20, error_messages=errors,
                                 widget=forms.PasswordInput(attrs={'placeholder': ' تکرار پسورد'}))

    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username__exact=user).values_list('username', ).exists():
            if User.objects.get(username__exact=user).is_active:
                raise forms.ValidationError('کاربری با این نام کاربری قبلا ایجاد شده است!')
        return user

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone__exact=phone).values_list('phone', ).exists():
            if User.objects.get(phone__exact=phone).is_active:
                raise forms.ValidationError('کاربری با این شماره همراه ایجاد شده است!')
        return phone

    def clean_password_2(self):
        pass_1 = self.cleaned_data['password_1']
        pass_2 = self.cleaned_data['password_2']
        if pass_2 != pass_1:
            raise forms.ValidationError('پسوردهای وارد شده متفاوتند!')
        else:
            return pass_2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['username', 'phone']

    def clean_password(self):
        return self.initial['password']


class LoginForm(forms.Form):
    phone = forms.IntegerField(error_messages=errors,
                               widget=forms.NumberInput(attrs={'placeholder': 'شماره همراه را وارد کنید'}))
    password = forms.CharField(max_length=20, error_messages=errors,
                               widget=forms.PasswordInput(attrs={'placeholder': 'پسورد را وارد کنید'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'image', 'bio', ]


# class ReceiveForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['phone', ]

class ForgetPasswordForm(forms.Form):
    number = forms.IntegerField(max_value=9999999999, min_value=9000000000, error_messages=errors,
                                widget=forms.NumberInput(attrs={'placeholder': 'شماره همراه را وارد کنید'}))
    username = forms.CharField(max_length=40,error_messages=errors,
                               widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))


class CodeForm(forms.Form):
    code = forms.IntegerField()
