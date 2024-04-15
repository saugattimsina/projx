from django.contrib import admin
from .models import User, UserKey

admin.site.register(UserKey)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "refered", "is_suscribed", "user_uuid"]
