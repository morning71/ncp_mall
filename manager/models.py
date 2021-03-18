from django.db import models

#商家信息表
class Manager(models.Model):
    class Meta:
        verbose_name = '商家'
        verbose_name_plural = '商家'
    manager_name = models.CharField(max_length=50,verbose_name='商家用户名')
    email = models.EmailField('商家邮箱')
    password = models.CharField(max_length=32,verbose_name='商家密码')
    image = models.ImageField(upload_to='media/manager/image',default='media/manager/image/default_picture.jpg')
    is_login = models.BooleanField(default=0)   #0代表未登录  1代表已登录

    def __str__(self):
        return  self.manager_name