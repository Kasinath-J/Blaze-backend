from django.contrib import admin
from .models import NewUser,Profile
from django.forms import Textarea
from django.db import models
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email','year')
    list_filter = ('year','is_active', 'is_staff')
    ordering = ('email',)
    list_display = ('email','year',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email','year')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','year', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

# # Register your models here.
admin.site.register(NewUser,UserAdminConfig)
admin.site.register(Profile)
