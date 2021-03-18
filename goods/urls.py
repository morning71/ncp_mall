from django.urls import path
from goods import views


urlpatterns = [
    path('index/',views.Index.as_view(),name="index"),
    path('list/',views.List.as_view(),name="list"),
    path('goods/',views.goods.as_view(),name="goods"),
    path('check_count/',views.check_count,name="check_count"),
    path('search/',views.search,name="search"),
    path('demo/vue/api/',views.DemoVueApi,name="DemoVueApi"),
    path('demo/',views.demo,name="demo"),
]
app_name='goods'