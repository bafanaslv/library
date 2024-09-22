from django.contrib import admin

from users.models import Users


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
        "tg_chat_id",
    )
