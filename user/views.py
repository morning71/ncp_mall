from django.shortcuts import render, redirect,render_to_response
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, QueryDict,FileResponse
from user.models import User, Carts, Order, Order_info,Address,Comment
from QSHOP.common import set_password
from QSHOP.common import user_login_valid
from goods.models import Goods
from django.views.decorators.csrf import csrf_exempt
import time
from QSHOP.common import set_page,Pay,send_manager_email
from django.http import Http404
from django.utils import timezone



# 注册
class Register(View):
    def get(self, request):
        if request.is_ajax():
            user_name = request.GET.get('user_name')
            result = {'flag': 1}
            user = User.objects.filter(user_name=user_name)
            if user.exists():
                result['flag'] = 0
            return JsonResponse(result)
        return render(request, 'user_common/register.html')

    def post(self, request):
        data = request.POST
        user_name = data.get('user_name')
        password = data.get('password')
        email = data.get('email')
        pwd = set_password(set_password(set_password(password)))
        u = User()
        u.user_name = user_name
        u.password = pwd
        u.email = email
        u.save()
        return redirect('user:login')


# 登录
class Login(View):

    def __init__(self):
        super(Login, self).__init__()
        self.message = ''

    def get(self, request):
        next = request.GET.get("next", "")
        refer = request.META.get("HTTP_REFERER")
        print(refer, 11111111)
        print(next)
        return render(request, 'user_common/login.html', {'message': self.message, 'next': next})

    def post(self, request):
        data = request.POST
        user_name = data.get('user_name')
        passwrod = data.get('password')
        pwd = set_password(set_password(set_password(passwrod)))
        u = User.objects.filter(user_name=user_name, password=pwd)
        if u.exists():
            request.session['user_name'] = user_name
            request.session['user_id'] = u[0].id
            next = data.get('next')
            if next:
                response = HttpResponseRedirect(next)
            else:
                response = HttpResponseRedirect('/goods/index')
            response.set_cookie('user_name', user_name)
            return response
        else:
            self.message = "用户名或密码有误！"
            return self.get(request)


# 退出
class Logout(View):
    def __int__(self):
        super(Logout, self).__init__()

    def get(self, request):
        response = redirect('user:login')
        try:
            del request.session['user_name']
            del request.session['user_id']
            response.delete_cookie('user_name')
        except:
            pass
        return response


# 购物车
class carts(View):
    def __init__(self):
        super(carts, self).__init__()
        self.result = {}

    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect('/user/login?next=/user/carts')
        goods_id = request.GET.get("goods_id",0)
        if goods_id:
            return self.add_car(request,'get')
        carts_list = Carts.objects.filter(user_id=user_id, goods__status=1, goods__goods_count__gt=0)
        return render(request, 'user_common/cart.html', {"carts_list": carts_list})

    def post(self, request):
        print(request.POST.get('type'))
        if request.POST.get('type') == "delete":
            return self.delete(request)
        return self.add_car(request,'post')

    def add_car(self, request,type):
        if type == "post":
            data = request.POST
            count = int(data.get('count'))
        else:
            data = request.GET
            count = 1
        user_id = request.session.get('user_id')
        visit_url = request.resolver_match.url_name
        print(visit_url, 1111111)
        if not user_id:
            return HttpResponseRedirect('/user/login')
        goods_id = data.get('goods_id')
        goods = Goods.objects.filter(id=goods_id, status=1, goods_count__gt=0)
        if goods.exists():
            goods = goods[0]
            Cart = Carts.objects.filter(user_id=user_id, goods_id=goods_id)
            if Cart.exists():
                c = Cart[0]
                if c.count + count <= goods.goods_count:
                    c.count += count
                else:
                    c.count = goods.goods_count
                c.save()
            else:
                c = Carts()
                if goods.goods_count >= count:
                    c.count = count
                else:
                    c.count = goods.goods_count
                c.user_id = user_id
                c.goods_id = goods_id
                c.save()
            return redirect('user:carts')
        return redirect('goods:list')

    def delete(self, request):
        data = request.POST
        carts_id = data.get("carts_id")
        user_id = request.session.get("user_id",None)
        if user_id:
            try:
                Carts.objects.get(id=carts_id,user_id=user_id).delete()
                self.result['status'] = 1   #删除成功
            except:
                self.result['status'] = 0   #删除失败
        else:
            self.result['status'] = 2       #未登录
        return JsonResponse(self.result)


# 购物车中检测库存
def carts_check_count(request):
    if request.method == "POST":
        data = request.POST
        carts_id = data.get('carts_id')
        count = int(data.get('count'))
        print("count", count)
        result = {'status': 1, "count": count}
        car = Carts.objects.filter(id=carts_id)
        if car.exists():
            car = car[0]
            if car.goods.status == 1 and car.goods.goods_count > 0:
                number = car.goods.goods_count
                if count >= number:
                    car.count = number
                    print(car.count, 111)
                    car.save()
                    result['data'] = number
                else:
                    car.count = count
                    car.save()
                    print(car.count, 2222222)
                    result['data'] = car.count
            else:
                result['status'] = 0
                result['data'] = '/user/carts'
        else:
            result['status'] = 0
            result['data'] = '/user/carts'
        return JsonResponse(result)
    return HttpResponse("请求方式有误！")


# 提交订单
@user_login_valid
def place_order(requet):
    if requet.method == "POST":
        user_id = requet.session.get('user_id')
        data = requet.POST
        result = []
        total_money = 0
        goods_id = data.get("goods_id",0)
        if goods_id:
            #直接购买
            count = int(data.get("count"))
            print(count,1111111111)
            goods_list = Goods.objects.filter(id=goods_id,status=1,goods_count__gte=count)
            for i in range(len(goods_list)):
                xiaoji = count * goods_list[i].goods_oprice
                result.append({
                    'number': i + 1,
                    'goods_id': goods_list[i].id,
                    'image': goods_list[i].goods_pic.url,
                    'goods_name': goods_list[i].goods_name,
                    'oprice': goods_list[i].goods_oprice,
                    'xprice': goods_list[i].goods_xprice,
                    'count': count,
                    'xiaoji': xiaoji
                })
                total_money += xiaoji
        else:
            #购物车进行结算
            carts = data.getlist('carts_name')
            car_list = Carts.objects.filter(id__in=carts, user_id=user_id, goods__status=1)

            for i in range(len(car_list)):
                xiaoji = car_list[i].count * car_list[i].goods.goods_oprice
                result.append({
                    'number': i + 1,
                    'id': car_list[i].id,
                    'image': car_list[i].goods.goods_pic.url,
                    'goods_name': car_list[i].goods.goods_name,
                    'oprice': car_list[i].goods.goods_oprice,
                    'xprice': car_list[i].goods.goods_xprice,
                    'count': car_list[i].count,
                    'xiaoji': xiaoji
                })
                total_money += xiaoji
        data = {}
        data['money'] = total_money
        data['result'] = result
        address_list = Address.objects.filter(user_id=user_id)
        return render(requet, 'user_common/place_order.html', {"data": data, "address_list": address_list})
    return HttpResponse("请求方式有误")


# 创建订单
@user_login_valid
def create_order(request):
    if request.method == "POST":
        data = request.POST
        address = data.get("address", 0)

        user_id = request.session.get("user_id")
        a = Address.objects.filter(id=address, user_id=user_id).first()
        if not a:
            return HttpResponse("请选择收货地址！")
        total_money = 0
        goods_id = data.get("goods_id")
        flag = False   #判断是直接购买还是从购物车中购买
        if goods_id:
            count  = int(data.get("count"))
            goods = Goods.objects.filter(id=goods_id,goods_count__gte=count,status=1).first()
            print(count,goods,111111111111111)
            if not goods:
                return HttpResponse("商品信息有误，请重新选择！")
            goods.goods_count -= count
            goods.save()
            total_money += goods.goods_oprice * count
            print("totalmone",total_money)
        else:
            carts_list = data.getlist("car_id")
            car_list = Carts.objects.filter(user_id=user_id, id__in=carts_list)
            if not car_list.exists():
                return HttpResponse("请选择商品！")

            # 判断库存是否充足
            for car in car_list:
                print(car.goods_id, car.count)
                goods = Goods.objects.filter(id=car.goods_id, status=1).first()
                if not goods:
                    return HttpResponse("商品已下架，请重新选择！")
                if car.count > goods.goods_count:
                    return HttpResponse("商品数量有误，请重新选择！")

            # 减少库存
            for car in car_list:
                goods = Goods.objects.filter(id=car.goods_id, status=1).first()
                goods.goods_count -= car.count
                goods.save()
                total_money += car.count * goods.goods_oprice
                print(total_money, 222222222)
            flag = True
        # 生成总订单
        total_code = ''.join(str(time.time()).split('.'))
        print(total_code, 22222222222)
        orderObj = Order()
        orderObj.total_code = total_code
        orderObj.user_id = user_id
        orderObj.contacts = a.username
        orderObj.address = a.address
        orderObj.phone = a.userphone
        orderObj.total_money = total_money
        orderObj.save()
        if flag:
            # 生成订单详情
            for car in car_list:
                order_code = set_password(total_code + str(car.id))
                orderinfoObj = Order_info()
                orderinfoObj.order_code = order_code
                orderinfoObj.order_id = orderObj.id
                orderinfoObj.goods_id = car.goods.id
                orderinfoObj.number = car.count
                orderinfoObj.money = car.goods.goods_oprice
                orderinfoObj.manager_id = car.goods.manager_id
                orderinfoObj.save()
                # 订单生成之后删除购物车的数据
                car_list.delete()
        else:
            order_code = set_password(total_code + str(goods.id))
            orderinfoObj = Order_info()
            orderinfoObj.order_code = order_code
            orderinfoObj.order_id = orderObj.id
            orderinfoObj.goods_id = goods.id
            orderinfoObj.number = count
            orderinfoObj.money = goods.goods_oprice
            orderinfoObj.manager_id = goods.manager_id
            orderinfoObj.save()
        r = Pay(total_code, str(total_money), "http://127.0.0.1:8000/user/return_url/")
        print("rrrrrr", r)
        return HttpResponseRedirect(r)
    return HttpResponse("请求方式有误！")



# 买家个人中心
class User_info(View):
    def __init__(self):
        super(View, self).__init__()

    def get(self, request):
        user_info = "active"
        user_id = request.session.get('user_id', '')
        if not user_id:
            return HttpResponseRedirect('/user/login?next=/user/user_info')
        user = User.objects.filter(id=user_id).first()
        return render(request, 'user_common/user_center_info.html', {"user_info": user_info, "user": user})

    def post(self):
        pass


# 买家订单中心
class User_order(View):
    def __init__(self):
        super(View, self).__init__()

    def get(self, request):
        user_id = request.session.get('user_id', '')
        if not user_id:
            return HttpResponseRedirect('/user/login?next=/user/user_order/')
        user_order = "active"
        order_list = Order.objects.filter(user_id=user_id)
        page = request.GET.get("page", 1)
        data, page_list = set_page(order_list, 1, page)
        return render(request, 'user_common/user_center_order.html',
                      {"user_order": user_order, "order_list": data, "page_list": page_list})


# 买家用户地址管理
class User_site(View):
    def __init__(self):
        super(View, self).__init__()

    def get(self, request):
        user_site = "active"
        user_id = request.session.get('user_id', '')
        if not user_id:
            return HttpResponseRedirect("/user/login?next=/user/user_site")
        address_list = Address.objects.filter(user_id=user_id)
        address_id = request.GET.get("address_id", 0)
        data = {}
        address = Address.objects.filter(user_id=user_id, id=address_id)
        if address:
            data['id'] = address[0].id
            data['username'] = address[0].username
            data['address'] = address[0].address
            data['phone'] = address[0].userphone
        return render(request, 'user_common/user_center_site.html',
                      {"user_site": user_site, "address_list": address_list, "data": data})

    def post(self, request):
        self.request = request
        data = self.request.POST
        user_id = self.request.session.get('user_id', '')
        if not user_id:
            return HttpResponseRedirect("/user/login?next=/user/user_site")
        address_id = data.get("address_id")
        username = data.get('username')
        address = data.get('address')
        userphone = data.get('userphone')
        if address_id:
            Address.objects.filter(user_id=user_id, id=address_id).update(
                username=username, address=address, userphone=userphone
            )
        else:
            a = Address()
            a.username = username
            a.address = address
            a.userphone = userphone
            a.user_id = user_id
            a.save()
        return HttpResponseRedirect('/user/user_site')


# 设置默认地址
@user_login_valid
def set_address(request):
    user_id = request.session.get('user_id', 0)
    if user_id:
        id = int(request.GET.get('id'))
        # print(id,user_id)
        Address.objects.exclude(id=id, user_id=user_id).update(isdefault=0)
        Address.objects.filter(id=id, user_id=user_id).update(isdefault=1)
        result = {"flag": 1}
    else:
        result = {"flag": 0}
    return JsonResponse(result)


# 为未支付的订单付款
@user_login_valid
def pay_order(request, order_id):
    user_id = request.session.get("user_id")
    print(user_id, 1111111)
    order = Order.objects.filter(id=order_id, user_id=user_id, pay_status=0)
    if order.exists():
        o = order[0]
        response = Pay(o.total_code, str(o.total_money), "http://127.0.0.1:8000/user/return_url/")
        return HttpResponseRedirect(response)
    raise Http404


# 支付成功的回调路由
def return_url(request):
    print(request, 1111111111111)
    out_trade_no = request.GET.get("out_trade_no")
    Order.objects.filter(total_code=out_trade_no).update(pay_status=1, pay_time=timezone.datetime.now())
    return HttpResponseRedirect('/user/carts')


# 查询购物车数量
def select_carts_count(request):
    user_id = request.session.get("user_id", 0)
    count = Carts.objects.filter(user_id=user_id).count()
    print(count, 1111)
    return JsonResponse({"count": count})


@user_login_valid
def receive_goods(request,orderinfo_id):
    user_id = request.session.get("user_id")
    o = Order_info.objects.filter(id=orderinfo_id,order__pay_status=1,send_status=1,order__user_id=user_id).update(receive_status=1,receive_time=timezone.now())
    if o:
        return redirect('user:user_order')
    return render(request,"common/404.html")


#商品评价
@user_login_valid
def comment(request,orderinfo_id):
    if request.method == "POST":
        print("1111111")
        user_id = request.session.get("user_id")
        data = request.POST
        orderinfo_id = data.get("orderinfo_id")
        goods_score = data.get("goods_score")
        service_score = data.get("service_score")
        logistics_score = data.get("logistics_score")
        is_anonymous = data.getlist("is_anonymous")
        if is_anonymous:
            is_anonymous = 1
        else:
            is_anonymous = 0
        content = data.get("content")
        orderinfoObj = Order_info.objects.filter(id=orderinfo_id,order__pay_status=1,receive_status=1,send_status=1).first()
        orderinfoObj.comment_status = 1
        orderinfoObj.save()
        Comment.objects.create(user_id=user_id,goods_score=goods_score,service_score=service_score,logistics_score=logistics_score,content=content,create_time=timezone.now(),orderinfo_id=orderinfo_id,is_anonymous=is_anonymous)
        print(orderinfo_id,goods_score,service_score,logistics_score,is_anonymous)
        return redirect("user:user_order")
    o = Order_info.objects.filter(id=orderinfo_id,order__pay_status=1,send_status=1,receive_status=1).first()
    return render(request,"user_common/comment.html",{"o":o})


#催单
def reminder(request,orderinfo_id):
    user_id =request.session.get("user_id")
    data = {"status":2}
    if user_id:
        o = Order_info.objects.filter(id=orderinfo_id,order__pay_status=1,send_status=0,order__user_id=user_id).first()
        r = send_manager_email(message="",receiver=[o.manager.email],html_message="{}用户，您好，订单：{}已经发起了催单，请您尽快查看。<a href='http://127.0.0.1:8000/manager/order_list/'>点击查看订单</a>".format(o.order.user,o.order_code))
        if r:
            data['status'] = 1
        else:
            data['status'] = 0
    return JsonResponse(data)


"""
以下为测试接口
"""
def test_time(request):
    print(timezone.datetime.now())
    return HttpResponse(11111111)


class Demo(View):
    def get(self, request):
        return HttpResponse(111111111)


def demo(request, id2):
    print(id2)
    print(request.is_ajax())
    print(request.resolver_match)
    return HttpResponse(11111111)
