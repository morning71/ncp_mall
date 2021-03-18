import hashlib
#加密
def set_password(pwd):
    md = hashlib.md5()
    md.update(pwd.encode('utf-8'))
    md5_pwd = md.hexdigest()
    return md5_pwd


#商家用户的登录校验
from django.http import HttpResponseRedirect
def login_valid(func):
    def inner(request,*args,**kwargs):
        #通过key值是否在session和cookie中去校验
        print('session:',request.session.keys())   #通过session的keys校验
        print('cookie',request.COOKIES)
        if 'manager_name' in request.session and 'manager' in request.COOKIES:
            return func(request,*args,**kwargs)
        return HttpResponseRedirect('/manager/login')
    return inner



# 发送邮件
from django.core.mail import send_mail
from QSHOP import settings
def send_manager_email(message,receiver,html_message=None):
    print(message,receiver)
    try:
        if html_message:
            result = send_mail("优选农产品",message,settings.EMAIL_HOST_USER,receiver,html_message=html_message)
        else:
            result = send_mail("优选农产品",message,settings.EMAIL_HOST_USER,receiver)
    except:
        result = 0
    return result


#买家用户的登陆校验
def user_login_valid(func):
    def inner(request,*args,**kwargs):
        #通过key值是否在session和cookie中去校验
        print('session:',request.session.keys())   #通过session的keys校验
        print('cookie',request.COOKIES)
        visit_url = request.resolver_match.url_name
        print(visit_url,111111111111)
        if 'user_name' in request.session and 'user_name' in request.COOKIES:
            return func(request,*args,**kwargs)
        return HttpResponseRedirect('/user/login?next=/user/carts')
    return inner



from django.core.paginator import Paginator
def set_page(data,num,page):
    """
    :param data: 所有的数据
    :param num:  每页的数据
    :param page: 当前的页码
    :return:
    """
    p = Paginator(data,num)
    number = p.num_pages
    page_range = p.page_range
    try:
        page = int(page)
        data = p.page(page)
    except:
        data = p.page(1)
    if page < 5:  # 一次只返回5个页码
        page_list = page_range[:5]
    elif page + 4 > number:
        page_list = page_range[-5:]
    else:
        page_list = page_range[page - 3:page + 2]
    return data,page_list



# 支付
from alipay import AliPay
def Pay(order_id,money,return_url=None):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6KVS4YuG3pFvhbQHtBLjsgWXNe/Xjg2CVCc4+SfiwMeakR/O5IqZqVPThEl9allFyEHPFK7Anofebe+OO0BdYdGfCSrW0R+B85lEfH5YL2ggy9yCWB3GPiffA6B+UM2nO8HRMs1ulcpUPosCfzIucJUgX1IQZxJmAyTHmXzSoJVtY/1WbpLsP/zQgp+cUkfFi3CFDGxz6ex3w1U2q9SxemiQvUYbnn1EC3Yv3E0APloRrsAm+XIvPKLMacSbfHcZJw9EcaF3uNfNYtKzHGObigAzF1EEZlRbwG5LeOQ/iPJvbLilMyefFamuwgCZDBDTVQmHwA9QrjWjHUdeLZyW6QIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
       MIIEpgIBAAKCAQEA6KVS4YuG3pFvhbQHtBLjsgWXNe/Xjg2CVCc4+SfiwMeakR/O5IqZqVPThEl9allFyEHPFK7Anofebe+OO0BdYdGfCSrW0R+B85lEfH5YL2ggy9yCWB3GPiffA6B+UM2nO8HRMs1ulcpUPosCfzIucJUgX1IQZxJmAyTHmXzSoJVtY/1WbpLsP/zQgp+cUkfFi3CFDGxz6ex3w1U2q9SxemiQvUYbnn1EC3Yv3E0APloRrsAm+XIvPKLMacSbfHcZJw9EcaF3uNfNYtKzHGObigAzF1EEZlRbwG5LeOQ/iPJvbLilMyefFamuwgCZDBDTVQmHwA9QrjWjHUdeLZyW6QIDAQABAoIBAQCTZXtXbwEqLlbMDT38NyOP/L7K64RUefaivp74LO8bWNtzKwX4AmBMydFvNOiC4sC1mgxLfFSJnGeum2Iv5B3GBfuO4Vds81twLSEZByt0DbMJtlHW5jZd1wES2TJum31i/O9AEqwHt0McxRH16KNHrRPvkJzX0O5U+46CjnUcS5rZXir/OSDHwcN/cBxGqNhaEVsSSsWME8YOsfhCrVlKgI3vfW8UrEp/KociczM+N9wH0NbUlDgo2J9WuvH6/QyYkrLyO4KY5Bs05odS3wn+SoItOMEL8qROQ1iF9b2H5zYc7Ahd1kDBKGTSLVMw5iXUGBons0+eUCUoveiQF3+hAoGBAPcczgsFo9YuR1QSAjh2BsM9BEG2FAn5/xg4HzJoHEtd8fM4MAnwCGECWkzvNE866OaFs743ReQga9Nds4eI5Cg8019m1XAifzvxLaAK+nkotO+fz/8cNKrwS9pYFXNq2XRVph05r+Z/sSfMUUt4IecfTwjPvlGsWzeNQPjfOfx1AoGBAPEDUm9lHFDLngNIQisiRhIb2yWicJVMqL00rFZVnV6zh3G1Tbbp6EV5zmXS8/wJpmYwoGZO6RLWkMPB4f6YS4Lgi9nEHSxxDaIYvcWPasGywrWQw5r7NWEG71BCLGEG0yOVbOImiHAfC52L1hALtOCH9o7F0Lw2quNdAX4Ks3IlAoGBAJJz/uVnZU9VxC5eMfS2dpGVgwVS3ROAl6AJ+utL6qD8P54PSeFJ4h1kYJJCHnVqi4e76+grJ//o+x6c5P7JsbbrPbbH4m1/9HpZGNpGR2YxKvLtez9NvyUkH0B7fdMWm2QoMrgVbVuliB/3JqMcwrMQyi2Fudz70l/dFomo+tvVAoGBAOZPuV/v7G4dFiOm0mxrtTAq5HGDWDij5//erO1XpSnRP5ZeniQ0RBzYOG8/dp4cDqJKx4zczYeN+QrIZREpMcegkqQH76T/Z/rFz9tRoL/29nARJYsdkbXlrZ0xjz0tC2lOqp02G12hnTTxYx80QKXr56YpzL1/NDBPOVTcHvztAoGBAL29jtznLilUpKZqv5rEaInlBk47SDqb91vjLrsi0nvFTFOspifGkhWJHGvo0RzcSVkRqNUXFamWups+nGjJYMgcOWtktsBaFDqjoOuhC3x5qBH6L/8mNuFCcaDU+I0oJVCvxPcTuzhNXdY0gUFzibsjn56InfJsx+jB7jxEkyan
    -----END RSA PRIVATE KEY-----'''

    alipay = AliPay(
        appid="2016092100561600",  # 支付宝app的id
        app_notify_url="",  # 回调视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,     #订单编号
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="优选农产品",
        return_url=return_url, #完成之后回调函数
        notify_url = None  # 可选, 不填默认None
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string
print(Pay("1111","200"))