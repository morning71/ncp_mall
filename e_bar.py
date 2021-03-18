# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 17:47
# @Author  : Morning-J
# @FileName: e_bar.py
# @Software: PyCharm
# @Github:morning71
from pyecharts import Bar,Map,Page,Pie,Line,Overlap,Style

import pymysql
page = Page()
db = pymysql.connect('localhost','root','morning321','qshop')
cursor = db.cursor()
select_sql = '''SELECT '20-30元',COUNT(0) FROM goods_goods WHERE (goods_xprice +0)<30 AND (goods_xprice+0) >20
UNION
SELECT '30-40元',COUNT(0) FROM goods_goods WHERE (goods_xprice +0)<40 AND (goods_xprice+0) >30
UNION
SELECT '40-50元',COUNT(0) FROM goods_goods WHERE (goods_xprice +0)<50 AND (goods_xprice+0) >40
UNION
SELECT '50元以上',COUNT(0) FROM goods_goods WHERE (goods_xprice +0)<60 AND (goods_xprice+0) >50;'''
cursor.execute(select_sql)
price_list = []
price_num = []
for i in cursor.fetchall():
    price_list.append(i[0])
    price_num.append(i[1])
style = Style(height=500,width=1200)
bar = Bar('商品价格区间分布',**style.init_style,background_color='#FF9999')
bar.add('商品售价',x_axis=price_list,yaxis_max=24700,yaxis_min=24000,y_axis=price_num,mark_point=['min','max'],is_legend_show=True)
line = Line()
line.add('商品售价',x_axis=price_list,y_axis=price_num,effect_scale=8,line_color='#99FF66')
overlap = Overlap(height=400,width=1000)
overlap.add(bar)
overlap.add(line)
page.add(overlap)
page.render(path=u'table.jpg')