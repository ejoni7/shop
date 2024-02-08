from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/<int:page>/', views.home, name='home'),
    path('product/<slug>/<int:id>/', views.product, name='product'),
    path('product_like/<int:id>/', views.product_like, name='product_like'),
    path('send_comment/<int:id>/', views.send_comment, name='send_comment'),
    path('add_item_to_card/<int:id>/', views.add_item_to_card, name='add_item_to_card'),
    path('add_to_card/<int:id>/', views.add_to_card, name='add_to_card'),
    path('mines_of_card/<int:id>/', views.mines_of_card, name='mines_of_card'),
    path('delete_item/<int:id>/', views.delete_item, name='delete_item'),
    path('card/', views.card, name='card'),
    path('pay/', views.pay, name='pay'),
]
