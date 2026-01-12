from django.contrib import admin
from users.models import User, AuthToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('id', 'email', 'first_name', 'last_name', 'middle_name')
        }),
        ('Security', {
            'fields': ('password_hash', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_revoked', 'expires_at', 'created_at')
    list_filter = ('is_revoked', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('id', 'token', 'created_at')
