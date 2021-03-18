from pyecharts import Page,Line,Bar,Geo,Map
# from pyecharts.globals import CurrentConfig

# CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/assets/"

page = Page()
map = Map("供应商地区分布图",width="900px",height="500px")
import pymysql
db = pymysql.connect('localhost','root','morning321','qshop')
cursor = db.cursor()

select_sql = 'SELECT goods_address,COUNT(goods_address) FROM goods_goods GROUP BY goods_address;'
cursor.execute(select_sql)
city_list = []
num_list = []
for i in cursor.fetchall():
    city_list.append(i[0])
    num_list.append(i[1])
map.add("",city_list,num_list,maptype='china',is_visualmap=True,visual_text_color="#000",is_label_show=True)
map.show_config()
map.render("./charts.html")