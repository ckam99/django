from django.contrib import admin

from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin)

from .forms import UserCreationForm, UserChangeForm
from .models import User, Confirmation


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'username', 'fullname',
                    'is_staff', 'is_active', 'created_at', 'last_login', 'confirmed_at')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'fullname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'code', 'created_at',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)
admin.site.register(Confirmation, ConfirmationAdmin)
