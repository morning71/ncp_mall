# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 17:10
# @Author  : Morning-J
# @FileName: e_test.py
# @Software: PyCharm
# @Github:morning71
from pyecharts import Bar,Map,Page,Pie
import pymysql
page = Page()
db = pymysql.connect('localhost','root','morning321','qshop')
cursor = db.cursor()
select_sql = 'SELECT goods_address,COUNT(0) FROM goods_goods GROUP BY goods_address;'
city = []
g_num = []
cursor.execute(select_sql)
for i in cursor.fetchall():
    city.append(i[0])
    g_num.append(i[1])
map = Map('供销商所在地统计',width=1200,height=600)
map.add('供销商所在地',city,g_num,visual_range=[0,50],maptype='china',is_visualmap=True,visual_text_color='#000')
type_list = ['新鲜水果','海鲜水产','猪牛羊肉','禽类单品','新鲜蔬菜','速冻食品']

select_sql2 = 'SELECT type_id,COUNT(0) FROM goods_goods GROUP BY type_id;'
type_num = []
cursor.execute(select_sql2)
for j in cursor.fetchall():
    type_num.append(j[1])
pie = Pie('商品种类统计',width=1200,height=600)
pie.add('商品种类',type_list,type_num,is_label_show=True,is_more_utils=True)
page.add(map)
page.add(pie)
page.render(path='charts.html')