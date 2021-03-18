from django.urls import path,re_path
from user import views

from django.views.decorators.csrf import csrf_exempt
from QSHOP.common import user_login_valid

urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Logout.as_view(),name='logout'),
    path('carts/',views.carts.as_view(),name ="carts"),
    path('user_info/',views.User_info.as_view(),name ="user_info"),
    path('user_order/',views.User_order.as_view(),name ="user_order"),
    path('user_site/',views.User_site.as_view(),name ="user_site"),
    path('set_address/',views.set_address,name ="set_address"),
    path('carts_check_count/',views.carts_check_count,name ="carts_check_count"),
    path('place_order/',views.place_order,name ="place_order"),
    path('create_order/',views.create_order,name ="create_order"),
    path('select_carts_count/',views.select_carts_count,name ="select_carts_count"),
    path('pay_order/<int:order_id>',views.pay_order,name ="pay_order"),
    path('test_time/',views.test_time,name ="test_time"),
    path('return_url/',views.return_url,name ="return_url"),
    path('receive_goods/<int:orderinfo_id>',views.receive_goods,name ="receive_goods"),
    path('comment/<int:orderinfo_id>',views.comment,name ="comment"),
    path('reminder/<int:orderinfo_id>',views.reminder,name ="reminder"),

]
app_name='user'

urlpatterns += [
    # 使用装饰器装饰类
    path('Demo/', user_login_valid(views.Demo.as_view()), name="Demo"),
    # re_path('demo/(\d+)/(?P<id2>\d+)',views.demo,name='demo'),
]