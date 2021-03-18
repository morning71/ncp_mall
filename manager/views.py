from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from QSHOP.common import set_password,login_valid,send_manager_email,set_page
from .models import Manager
from goods.models import Type,Goods
import json
from django.http import JsonResponse
import random
from user.models import Order,Order_info
from django.utils import timezone


@login_valid
def index(request):
    return render(request,'common/index.html')

@login_valid
def charts(request):
    return render(request,'common/charts.html')

@login_valid
def table(request):
    return render(request,'common/table.html')

#注册
def register(request):
    error = ''
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        print(username,email,password1,password2)
        if password1 != password2:
            error =  '两次密码不一致！'
            return render(request, 'common/register.html', {"error": error})
        md5_pwd = set_password(set_password(password1))
        #对用户名需要加校验：看当前的用户名是否已经注册
        m = Manager.objects.filter(manager_name=username)
        if not m.exists():
            m = Manager.objects.create(manager_name=username,email=email,password=md5_pwd)
            return HttpResponseRedirect('/manager/login')
        error = '用户名重复'
    return render(request,'common/register.html',{"error":error})


#检测用户名是否重复
def check_username(request):
    result = {'flag':0 }
    data = request.GET
    username = data.get('username')
    if username != '':
        m = Manager.objects.filter(manager_name = username)
        if not m.exists():
            result['flag'] = 1   #0代表用户名重复，1代表用户名无重复
    #返回json对象的两种方式：
    #第一种：通过json.dumps()进行转化
    # return HttpResponse(json.dumps(result))
    #第二种：通过JsonResponse返回。
    return JsonResponse(result)


#登录
def login(request):
    error = ''
    if request.method == 'POST':
        data = request.POST
        manager_name = data.get('username')
        password = data.get('password')
        print(manager_name,password)
        md5_pwd =set_password(set_password(password))
        print(md5_pwd)
        try:
            m = Manager.objects.get(manager_name=manager_name,password=md5_pwd)
            #设置session  设置给request
            request.session['manager_name'] = manager_name
            request.session['id'] = m.id
            #设置cookie  设置给response
            response = HttpResponseRedirect('/manager/index')
            response.set_cookie('manager',manager_name)
            return response
        except:
            error = '用户名或者密码有误！'
    return render(request,'common/login.html',{'error':error})


#退出
def logout(request):
    response = HttpResponseRedirect('/manager/login')
    try:
        del request.session['id']               #删除商家session
        del request.session['manager_name']     #删除买家session
        response.delete_cookie('manager')       # 删除cookie
    except:
        pass
    return response


@login_valid
def add_goods(request):
    if request.method == "POST":
        data = request.POST
        # 接收数据通过在前端定义的name属性接收，接收不到时值为None
        goods_name = data.get('goods_name')
        goods_oprice = data.get('goods_oprice')
        goods_xprice = data.get('goods_xprice')
        goods_count = data.get('goods_count')
        goods_production = data.get('goods_production')
        safe_date = data.get('safe_date')
        goods_method = data.get('goods_method')
        goods_description = data.get('goods_description')
        # 文件类型数据的获取方式
        goods_pic = request.FILES.get('goods_pic')
        goods_address = data.get('goods_address')
        goods_info = data.get('goods_info')
        manager_id = request.session.get('id')
        type = data.get('type')
        status = data.get('status')
        Goods.objects.create(  # 添加进数据库
            goods_name=goods_name,
            goods_oprice=goods_oprice,
            goods_xprice=goods_xprice,
            goods_count=goods_count,
            goods_production=goods_production,
            safe_date=safe_date,
            goods_method=goods_method,
            goods_description=goods_description,
            # 文件类型数据的获取方式
            goods_pic=goods_pic,
            goods_address=goods_address,
            goods_info=goods_info,
            # manager_id = manager_id,
            manager=Manager.objects.get(id=manager_id),
            type_id=type,
            status=status,
        )
        return HttpResponse('商品添加成功！')
    type_list = Type.objects.all()
    return render(request, 'common/add_goods.html', {'type_list': type_list})


@login_valid
def goods_list(request):
    manager_id = request.session.get('id')
    goods_list = Goods.objects.filter(manager_id=manager_id).order_by('-status')
    print(goods_list)
    page = request.GET.get("page", 1)
    data, page_list = set_page(goods_list, 50, page)
    return render(request,'common/goods_list.html',{'goods_list':data,"page_list":page_list})


@login_valid
def goods_detail(request,id):
    manager_id = request.session.get('id')
    goods = Goods.objects.filter(id=id,manager_id=manager_id)
    if goods.exists():
        goods = goods[0]
        return render(request,'common/goods_detail.html',{'goods':goods})
    return render(request,'common/404.html')


@login_valid
def update_status(request,id):
    manager_id =request.session.get('id')
    goods  = Goods.objects.filter(id=id,manager_id=manager_id)
    if goods.exists():
        goods = goods[0]
        if goods.status == 1:
            goods.status = 0
        else:
            if goods.goods_count>0:
                goods.status = 1
        goods.save()     #保存数据
        return HttpResponseRedirect('/manager/goods_list')
    return render(request,'common/404.html')


@login_valid
def manager_message(request):
    manager_id = request.session.get('id')
    message = ""
    if request.method == "POST":
        o_pwd = request.POST.get('original_password')
        c_pwd = request.POST.get('current_password')
        o_md5 = set_password(set_password(o_pwd))
        m = Manager.objects.filter(id=manager_id,password=o_md5)
        if m.exists():
            c_md5 = set_password(set_password(c_pwd))
            # m.update(password=c_md5)
            c = m[0]
            c.password = c_md5
            c.save()
            return redirect('manager:login')
        message = "密码修改失败，原密码输入有误！"
    manager = Manager.objects.filter(id=manager_id)
    return render(request,'common/manager_message.html',{'manager':manager[0],'message':message})


@login_valid
def update_message(request):
    manager_id = request.session.get('id')
    manager = Manager.objects.filter(id=manager_id)
    if request.method == "POST":
        m = manager[0]
        data = request.POST
        manager_name = data.get('manager_name')
        email = data.get('email')
        image = request.FILES.get('image')
        m.manager_name = manager_name
        m.email = email
        if image:
            m.image = image
        m.save()
        return redirect('manager:manager_message')
    return render(request,'common/update_message.html',{'manager':manager[0]})


@login_valid
def update_goods(request,id):
    manager_id = request.session.get('id')
    if request.method == "POST":
        data = request.POST
        goods_id = data.get('goods_id')
        goods_name = data.get('goods_name')
        goods_oprice = data.get('goods_oprice')
        goods_xprice = data.get('goods_xprice')
        goods_count = data.get('goods_count')
        safe_date = data.get('safe_date')
        goods_method = data.get('goods_method')
        goods_description = data.get('goods_description')
        # 文件类型数据的获取方式
        goods_pic = request.FILES.get('goods_pic')
        goods_address = data.get('goods_address')
        goods_info = data.get('goods_info')
        type = data.get('type')
        status = data.get('status')
        manager_id = request.session.get('id')
        goods = Goods.objects.get(manager_id=manager_id,id=goods_id)
        goods.goods_name = goods_name
        goods.goods_oprice = goods_oprice
        goods.goods_xprice = goods_xprice
        goods.goods_count = goods_count
        goods.safe_date = safe_date
        goods.goods_method = goods_method
        goods.goods_description = goods_description
        # 文件类型数据的获取方式
        if goods_pic:
            goods.goods_pic = goods_pic
        goods.goods_address = goods_address
        goods.goods_info = goods_info
        goods.type_id = type
        goods.status = status
        goods.save()
        return redirect('manager:goods_detail',goods_id)
    type_list = Type.objects.all()
    goods = Goods.objects.filter(id=id,manager_id=manager_id)
    if goods.exists():
        return render(request,'common/update_goods.html',{'goods':goods[0],'type_list':type_list})
    return render(request,'common/404.html')


#重置密码
def forget_password(request):
    message = ''
    if request.method == "POST":
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        code = data.get('code')
        if code and email == request.session.get('email') and code.lower() == request.session.get('code'):
            md5_pwd = set_password(set_password(password))
            m = Manager.objects.filter(email=email).update(password=md5_pwd)
            del request.session['email']
            del request.session['code']
            return HttpResponseRedirect('/manager/login')
        message = "验证码或者邮箱有误！"
    return render(request, 'common/forget_password.html',{'message':message})


#发送验证码
def send_message(request):
    email = request.GET.get('email')
    m = Manager.objects.filter(email=email)
    res = {'flag':0,'data':'请输入正确的邮箱地址！'}
    if m.exists():
        candidate_string = 'ABC1D2EF3GH4IJ5KL6MN70PQ8RS9TUV0WXYZ'  # 候选字符串
        message = ''
        # 生成验证码
        for i in range(0, 5):
            one_str = candidate_string[random.randint(0, len(candidate_string) - 1)]
            message += one_str
        request.session['email'] = email
        request.session['code'] = message.lower()
        result = send_manager_email(message,[email])
        print("result", result)
        if result:
            res['flag'] = 1
            res['data'] = "邮件发送成功，请查收！"
    return JsonResponse(res)


#订单列表
@login_valid
def order_list(request):
    manager_id = request.session.get("id")
    orderinfo_list = Order_info.objects.filter(manager_id=manager_id)
    page=request.GET.get("page",1)
    data,page_list=set_page(orderinfo_list,1,page)
    return render(request,'common/order_list.html',{'orderinfo_list':data,"page_list":page_list})


#发货操作
@login_valid
def send_goods(request,orderinfo_id):
    manager_id = request.session.get("id")
    o = Order_info.objects.filter(id=orderinfo_id,order__pay_status=1,manager_id=manager_id).update(send_status=1,send_time= timezone.now())
    if o:
        return redirect('manager:order_list')
    return render(request,"common/404.html")


@login_valid
def order_detail(request,orderinfo_id):
    manager_id = request.session.get("id")
    o = Order_info.objects.filter(id=orderinfo_id,manager_id=manager_id).first()
    if o:
        return render(request,"common/order_detail.html",{"o":o})
    else:
        return render(request,"common/404.html")

import pymysql
@login_valid
def index_num(request):
    db = pymysql.connect('localhost','root','morning321','qshop')
    manager_id = request.session.get('id')
    print(manager_id)
    if manager_id is None:
        return render(request, "common/index.html")
    else:
        select_sql1 = 'SELECT SUM(number*money) AS total_money,COUNT(0) FROM user_order_info WHERE manager_id = "%s";' % manager_id
        cursor = db.cursor()
        cursor.execute(select_sql1)
        temp1 = cursor.fetchone()
        k = {}
        k['total'] = temp1[0]
        k['order_num'] = temp1[1]
        select_sql2 = 'SELECT COUNT(0) FROM goods_goods WHERE manager_id = "%s";' % manager_id
        cursor.execute(select_sql2)
        temp2 = cursor.fetchone()
        k['goods_num'] = temp2[0]
        select_sql3 = 'SELECT count(0) FROM user_order_info WHERE send_status = 1 AND manager_id = "%s";' %manager_id
        cursor.execute(select_sql3)
        temp3 = cursor.fetchone()
        k['send_num'] = "{:.002f}%".format(int(temp3[0])/int(temp1[1])*100)
        print(k)
        return render(request,"common/index.html",{"k":k})
    # kk = k.aggregate()
    # print(k)

from pyecharts import Page,Map,Pie
# from pyecharts.constants import
from django.template import loader
# from pyecharts.constan

@login_valid
def charts(request):
    templ = loader.get_template('common/charts.html')
    p = charts_M()
    context = dict(
        myechart=p.render_embed(),
        # scripe_list = p.get_js_dependencies()
    )
    return HttpResponseRedirect(templ.render(context,request))

def charts_M():
    import pymysql
    page = Page()
    db = pymysql.connect('localhost', 'root', 'morning321', 'qshop')
    cursor = db.cursor()
    select_sql = 'SELECT goods_address,COUNT(0) FROM goods_goods GROUP BY goods_address;'
    city = []
    g_num = []
    cursor.execute(select_sql)
    for i in cursor.fetchall():
        city.append(i[0])
        g_num.append(i[1])
    map = Map('供销商所在地统计', width=1200, height=600)
    map.add('供销商所在地', city, g_num, visual_range=[0, 50], maptype='china', is_visualmap=True, visual_text_color='#000')
    type_list = ['新鲜水果', '海鲜水产', '猪牛羊肉', '禽类单品', '新鲜蔬菜', '速冻食品']

    select_sql2 = 'SELECT type_id,COUNT(0) FROM goods_goods GROUP BY type_id;'
    type_num = []
    cursor.execute(select_sql2)
    for j in cursor.fetchall():
        type_num.append(j[1])
    pie = Pie('商品种类统计', width=1200, height=600)
    pie.add('商品种类', type_list, type_num, is_label_show=True, is_more_utils=True)
    page.add(map)
    page.add(pie)
    return page