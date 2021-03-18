from django.shortcuts import render
from django.views import View
from goods.models import Type, Goods
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from QSHOP.common import set_page
from django.db.models import Q
from user.models import Hobby
from django.views.decorators.csrf import csrf_exempt


# 首页
class Index(View):
    def get(self, request):
        type_list = Type.objects.all()
        goods = {}
        for type in type_list:
            goods[type.id] = Goods.objects.filter(type_id=type.id, status=1, goods_count__gt=0)[:4]
        print(goods)
        return render(request, 'goods_common/index.html', {"goods": goods})


# 商品列表
class List(View):
    def __init__(self):
        super(List, self).__init__()
        self.result = {
            'code': 200,
            'data': [],
            'page_range': [],
            'p': 1,
            'page_next': False,
            'page_previous': False,
        }
        self.message = ""

    def get(self, request):
        t_id = request.GET.get('t_id', 0)
        try:
            t_id = int(t_id)
        except:
            t_id = 0
        goods_name = request.GET.get("name", '')
        self.message = goods_name
        if request.is_ajax():
            if 0 < t_id < 7:
                goods_list = Goods.objects.filter(type_id=t_id, status=1, goods_count__gt=0)
            else:
                goods_list = Goods.objects.filter(status=1, goods_count__gt=0)
            if goods_name:
                goods_list = goods_list.filter(
                    (Q(goods_name__contains=goods_name) | Q(type__type_name__contains=goods_name)), status=1,
                    goods_count__gte=1)
            try:
                page = int(request.GET.get('page', 1))
            except:
                page = 1
            data, page_range = set_page(goods_list, 10, page)
            if data.has_next():
                page_next = data.next_page_number
                self.result['page_next'] = page_next()
            if data.has_previous():
                page_previous = data.previous_page_number
                self.result['page_previous'] = page_previous()
            for goods in data:
                dict1 = {
                    'id': goods.id,
                    'goods_name': goods.goods_name,
                    'goods_pic': goods.goods_pic.url,
                    'goods_oprice': goods.goods_oprice,
                    'goods_xprice': goods.goods_xprice,
                }
                self.result['data'].append(dict1)
            self.result['page_range'] = list(page_range)
            self.result['p'] = page
            print(self.result)
            return JsonResponse(self.result)
        return render(request, 'goods_common/list.html', {"t_id": t_id, "name": self.message})


# 商品搜索
def search(request):
    data = request.GET
    goods_name = data.get("name")
    return HttpResponseRedirect("/goods/list/?name={}".format(goods_name))


# 商品详情
class goods(View):
    def __int__(self):
        super(goods, self).__init__()

    def get(self, request):
        goods_id = request.GET.get('goods_id')
        if goods_id:
            goods = Goods.objects.filter(id=goods_id, status=1, goods_count__gt=0)
            if goods.exists():
                goods = goods[0]
                goods_list = Goods.objects.filter(status=1, goods_count__gt=0, type_id=goods.type_id).exclude(
                    id=goods_id)[:2]
                return render(request, 'goods_common/detail.html', {'goods': goods, 'goods_list': goods_list})
        raise Http404


# 加购之前检测库存
def check_count(request):
    if request.method == "POST":
        data = request.POST
        goods_id = data.get('goods_id')
        count = int(data.get('count'))
        goods = Goods.objects.filter(id=goods_id, status=1, goods_count__gt=0)
        result = {}
        if goods.exists():
            goods = goods[0]
            status = 1
            if count > goods.goods_count:
                count = goods.goods_count
            result['count'] = count
        else:
            status = 0
        result['status'] = status
        return JsonResponse(result)
    return HttpResponse("请求方式有误！")


#vue示例
import json
@csrf_exempt
def DemoVueApi(request):
    if request.method=="POST":
        data = json.loads(request.body.decode("utf-8"))
        print(data.get("firstName"))
        r = {"data":1}
        return JsonResponse(r)
    return render(request,'demo_vue.html')



# 测试 process_exception
def demo(request):
    Goods.objects.get(id=1000000000000)
    return HttpResponse("1111")