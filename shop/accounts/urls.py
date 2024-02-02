from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    # path('login_api/', obtain_auth_token, name='auth_token'),
    path('logout_/', views.logout_, name='logout_'),
    path('register/', views.register, name='register'),
    path('phone_check/', views.phone_check, name='phone_check'),
    path('profile/', views.profile, name='profile'),
    path('rules/', views.Rules.as_view(), name='rules'),
    # path('ends/', views.Ends.as_view(), name='ends'),
    path('change_password/', views.change_password, name='change_password'),
    # path('forget_password/', views.ForgetPassword.as_view(), name='forget_password'),
    # path('password_reset_done/', views.ResetDone.as_view(), name='password_reset_done'),
    # path('confirm_password/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='confirm_password'),
    # path('confirm_done/', views.ConfirmDone.as_view(), name='confirm_done'),
    path('forget_password/', views.forget_password, name='forget_password'),

]
