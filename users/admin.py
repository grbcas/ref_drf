from django.contrib import admin

from users.models import User

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'own_invite_key',
        'related_user',
        'invite_key',
        'is_active'
    )
