from django.contrib import admin
from .models import Manager

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['id','manager_name','email',]
    list_display_links = ['id']   #控制哪个字段可以进入编辑页面