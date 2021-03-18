from django.db import models
from goods.models import Goods
from manager.models import Manager


#卖家用户表
class User(models.Model):
    class Meta:
        verbose_name = "买家用户"
        verbose_name_plural = "买家用户"

    user_name = models.CharField(max_length=20)
    email = models.EmailField('买家邮箱')
    password = models.CharField(max_length=32,verbose_name='买家密码')
    image = models.ImageField(upload_to='media/user/image',default='media/user/image/user_default.jpg')
    is_login = models.BooleanField(default=0)

    def __str__(self):
        return self.user_name


#购物车表
class Carts(models.Model):
    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = "购物车"
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='买家')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="商品")
    count = models.IntegerField('数量')


#收货地址表
class Address(models.Model):
    class Meta:
        verbose_name = "收获地址"
        verbose_name_plural = "收获地址"
    username = models.CharField(max_length=25,verbose_name="收货人姓名")
    userphone = models.CharField(max_length=20,verbose_name="收货人电话")
    address = models.CharField(max_length=255, verbose_name="详细地址")
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="买家")
    isdefault = models.BooleanField(default=0,verbose_name="是否默认地址")        #0否，1是
    createtime = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")


#订单总表
class Order(models.Model):
    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
    total_code = models.CharField(max_length=17,unique=True,verbose_name="订单总编号")
    user = models.ForeignKey(User,verbose_name="买家",on_delete=models.DO_NOTHING)
    add_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    contacts = models.CharField(max_length=30, verbose_name="收货人")
    address = models.CharField(max_length=255,verbose_name="收货地址")
    phone = models.CharField(max_length=20,verbose_name="收货人电话")
    pay_status = models.BooleanField(default=0,verbose_name="支付状态")  #默认为0，未支付
    pay_time = models.DateTimeField(null=True,verbose_name="支付时间")
    total_money = models.FloatField(verbose_name="价格")
    def __str__(self):
        return self.total_code


#订单详情表
class Order_info(models.Model):
    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = "订单详情"
    order_code = models.CharField(max_length=32,verbose_name="订单详细编号")
    order = models.ForeignKey(Order,verbose_name="订单", on_delete=models.DO_NOTHING)
    goods = models.ForeignKey(Goods,verbose_name="商品", on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=1, verbose_name="数量")
    money = models.FloatField(verbose_name="价格")
    send_status = models.BooleanField(default=0,verbose_name="发货状态")
    send_time = models.DateTimeField(null=True,verbose_name="发货时间")
    receive_status = models.BooleanField(default=0, verbose_name="收货状态")
    receive_time = models.DateTimeField(null=True, verbose_name="收货时间")
    comment_status = models.BooleanField(default=0, verbose_name="评价状态")
    manager = models.ForeignKey(Manager, verbose_name="商家", on_delete=models.DO_NOTHING)


#用户爱好表
class Hobby(models.Model):
    class Meta:
        verbose_name = "买家爱好"
        verbose_name_plural = "买家爱好"
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='买家')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="商品")


#用户评价表
class Comment(models.Model):
    class Meta:
        verbose_name = "商品评价"
        verbose_name_plural = "商品评价"
    goods_score = models.FloatField(verbose_name="商品评分")
    service_score = models.FloatField(verbose_name="客服评分")
    logistics_score = models.FloatField(verbose_name="物流评分")
    content = models.TextField(verbose_name="评价内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评价时间")
    shop_reply = models.TextField(verbose_name="商家回复")
    reply_time = models.DateTimeField(null=True, verbose_name="商家回复时间")
    user = models.ForeignKey(User,verbose_name="买家用户",on_delete=models.CASCADE)
    orderinfo = models.ForeignKey(Order_info,on_delete=models.CASCADE,verbose_name="订单详情")
    is_anonymous = models.BooleanField(verbose_name="是否匿名评价")