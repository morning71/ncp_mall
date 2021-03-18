from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'email', ]
    list_display_links = ['id']  # 控制哪个字段可以进入编辑页面
