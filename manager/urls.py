from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('index/',views.index_num,name='index'),
    path('register/',views.register,name='register'),
    path('check_username/',views.check_username,name='check_username'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('add_goods/',views.add_goods,name='add_goods'),
    path('goods_list/',views.goods_list,name='goods_list'),
    path('goods_detail/<int:id>',views.goods_detail,name='goods_detail'),
    path('update_status/<int:id>',views.update_status,name='update_status'),
    path('manager_message/',views.manager_message,name='manager_message'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('send_message/',views.send_message,name='send_message'),
    path('update_goods/<int:id>',views.update_goods,name='update_goods'),
    path('update_message/',views.update_message,name='update_message'),
    path('order_list/',views.order_list,name='order_list'),
    path('send_goods/<int:orderinfo_id>',views.send_goods,name='send_goods'),
    path('order_detail/<int:orderinfo_id>',views.order_detail,name='order_detail'),
    path('charts/',TemplateView.as_view(template_name='common/charts.html'),name='charts'),
    path('table/',TemplateView.as_view(template_name='common/table.html'),name='table')
]
app_name='manager'