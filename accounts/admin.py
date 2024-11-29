from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminCustom(UserAdmin):
    # 詳細
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "username",
                    "email",
                    "password",
                    "avatar",
                    "introduction",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "updated_at",
                    "created_at",
                )
            },
        ),
    )

    # 追加
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # 一覧
    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "updated_at",
        "created_at",
    )

    list_filter = ()
    # 検索
    search_fields = (
        "id",
        "email",
    )
    # 順番
    ordering = ("updated_at",)
    # リンク
    list_display_links = ("id", "username", "email")
    # 編集不可
    readonly_fields = ("updated_at", "created_at", "id")


admin.site.register(User, UserAdminCustom)