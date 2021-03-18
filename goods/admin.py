from django.contrib import admin
from  .models import Type,Goods

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','type_name','date']
    date_hierarchy = 'date'   #根据日期数据进行分类，实现快捷搜索功能
    list_display_links = ['type_name']   #控制哪个字段可以进入编辑页面



@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id','goods_name','manager',"goods_count"]
    list_display_links = ['id']   #控制哪个字段可以进入编辑页面
