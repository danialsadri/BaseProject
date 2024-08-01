from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from jalali_date.admin import ModelAdminJalaliMixin
from .forms import UserCreationForm, UserChangeForm
from .models import UserModel


@admin.register(UserModel)
class UserAdmin(ModelAdminJalaliMixin, BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        'phone_number', 'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser'
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['phone_number', 'email']
    readonly_fields = ['login_time']
    raw_id_fields = ['photo']
    filter_horizontal = ['groups', 'user_permissions']

    fieldsets = (
        ('اطلاعات', {'fields': [
            'phone_number', 'email',
            'first_name', 'last_name', 'photo',
            'password',
        ]}),
        ('دسترسی ها', {'fields': [
            'is_active', 'is_staff', 'is_superuser',
            'login_time', 'groups', 'user_permissions',
        ]}),
    )

    add_fieldsets = (
        (None, {'fields': [
            'phone_number', 'password',
        ]}),
    )
