from django.contrib import admin
from .models import NewUser,Profile,LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail,Event,Problem,OfficeBearer
from django.forms import TextInput, Textarea, CharField
from django.db import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.

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
admin.site.register(LeetcodeDetail)
admin.site.register(GithubDetail)
admin.site.register(LinkedInDetail)
admin.site.register(HackerrankDetail)
admin.site.register(CodechefDetail)
admin.site.register(CodeforcesDetail)
admin.site.register(Event)   
admin.site.register(Problem)   
admin.site.register(OfficeBearer)    