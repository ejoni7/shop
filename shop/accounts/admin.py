from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as base
from django.contrib.auth.models import Group
from .form import *
from product.admin import ItemInline
import admin_thumbnails


# Register your models here.
@admin_thumbnails.thumbnail('image')
class UserAdmin(base):
    form = UserChangeForm
    add_form = UserCreatForm
    list_display = ('id', 'username', 'image_thumbnail', 'is_active','created','is_admin','image',)
    list_editable = ('is_active','image',)
    list_filter = ('username',)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    fieldsets = (
        ('user', {'fields': ('username', 'phone', 'image_thumbnail','bio',)}),
        ('status', {'fields': ('is_active', )})
    )
    inlines=[ItemInline,]
    add_fieldsets = (
        (None, {'fields': ('username', 'phone', 'password1', 'password2')}),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
