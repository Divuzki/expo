from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from profiles.models import Profile
from .models import User  # , user_type

# Inline + descriptor


class AdminProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name',
         'username', 'password', 'email', 'last_login')}),
        ('Permissions', {'fields': (
            'is_verified',
            'is_show_full_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('username', 'email', 'is_staff',
                    'is_verified', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups', 'is_verified')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    # Define new admin with inline
    inlines = (AdminProfileInline,)


# Register UserAdmin
admin.site.register(User, UserAdmin)

# We can register our models like before
# This was the model we commented in the previous snippet.

# admin.site.register(user_type)
