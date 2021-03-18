from django.db import models
from manager.models import  Manager

class Type(models.Model):
    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = '商品类别'
    type_name = models.CharField(max_length=50,verbose_name='类别名称')
    date = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    def __str__(self):
        return  self.type_name


class Goods(models.Model):
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

    goods_name = models.TextField(verbose_name='商品名称')
    goods_oprice = models.FloatField(verbose_name='现价')
    goods_xprice = models.FloatField(verbose_name='原价')
    goods_count = models.IntegerField(default=0,verbose_name='商品数量')
    goods_production = models.DateTimeField(auto_now=True,verbose_name='生产日期')
    safe_date = models.CharField(max_length=10,verbose_name='保质期')
    goods_method = models.CharField(max_length=100,verbose_name='存储方法')
    goods_description = models.TextField(verbose_name='商品简介')
    goods_pic = models.ImageField(upload_to='media/goods/image',verbose_name='商品图片')
    goods_address = models.CharField(max_length=50,verbose_name='配送地址')
    goods_info = models.TextField(verbose_name='商品详情')
    manager = models.ForeignKey(Manager,on_delete=models.CASCADE,verbose_name='商家')
    type = models.ForeignKey(Type,on_delete=models.CASCADE,verbose_name='类别')
    status = models.BooleanField(default=1,verbose_name='商品状态')   #0代表下架，1代表上架

    def __str__(self):
        return self.goods_name   #外键关联时直接通过外键显示商品名称
