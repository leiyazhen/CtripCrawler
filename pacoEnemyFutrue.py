#coding=utf-8
from bs4 import BeautifulSoup
from urllib import parse
import urllib
from urllib.request import quote
from urllib.request import urlopen
import re;
from HttpClient import httpCall;
import json;
import datetime;
import sys,os;
import xlrd,xlwt;
from xlrd import open_workbook
from xlutils.copy import copy
import time
import requests
import execjs
import json


headers_ocean = {
    'host': 'hotels.ctrip.com',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'referer': 'https://hotels.ctrip.com/hotel/438080.html',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
headers = {
    'host': 'hotels.ctrip.com',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'if-modified-since': 'Thu, 01 Jan 1970 00:00:00 GMT',
    'referer': 'https://hotels.ctrip.com/hotel/438080.html',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
def get_callback():
    """拿到callback，算出来的一个随机15位字符串"""
    callback = """
        var callback = function() {
        for (var t = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], o = "CAS", n = 0; n < 15; n++) {
            var i = Math.ceil(51 * Math.random());
            o += t[i]
        }
        return o
        };
            """
    js = execjs.compile(callback)
    return js.call('callback')


def deal_ocean(js_txt, hotel_id, call_back):
    """处理js_txt"""
    # 第一步先还原
    js_txt = re.sub('eval', 'return', js_txt)
    js_1 = execjs.compile(js_txt)
    ocean_txt = js_1.call('f')

    # 第二部开始处理这段js,要在execjs里执行，需要添加一些头
    # 先补充变量,需要知道hotel_id

    variable = """
            var hotel_id = "%s";
            var site = {};
            site.getUserAgent = function(){};
            var Image = function(){};
            var window = {};
            window.document = {body:{innerHTML:"1"}, documentElement:{attributes:{webdriver:"1"}}, createElement:function(x){return {innerHTML:"1"}}};
            var document = window.document;
            window.navigator = {"appCodeName":"Mozilla", "appName":"Netscape", "language":"zh-CN", "platform":"Win"};
            window.navigator.userAgent = site.getUserAgent();
            var navigator = window.navigator;
            window.location = {};
            window.location.href = "http://hotels.ctrip.com/hotel/%s.html";
            var location = window.location;
            var navigator = {userAgent:{indexOf: function(x){return "1"}}, geolocation:"1"};
            """% (hotel_id, hotel_id)

    # 第三步开始改造js
    js_final = ''
    js_final += variable
    ocean_txt = re.sub(';!function', 'function get_eleven', ocean_txt)
    js_final += ocean_txt[:-3]
    rep_cnt = re.findall('{0}.*?";\'\)\)'.format(call_back), js_final, re.S)[0]
    eleven = rep_cnt.split('+')[1]
    # 然后替换
    js_final = js_final.replace(rep_cnt, 'return{0}'.format(eleven))
    # 找到嘲讽那段，然后替换
    sneer = re.findall(' \[32769,26495,32473.*,49,51,107,21734]\*/', js_final, re.S)[0]
    js_final = js_final.replace(sneer, '=1);')
    # 第四部，执行
    js_content = execjs.compile(js_final)
    return js_content.call('get_eleven')


def main_logic(hotel_id):
    # 1. 拿到callback和时间戳请求ocean.js
    while True:
        try:
            print('重试.....')
            call_back = get_callback()
            t = int(time.time()*1000)
            ocean_js = request_oceanball(call_back, t)
            # 接下来处理ocean_js
            eleven = deal_ocean(ocean_js, hotel_id, call_back)
            break
        except Exception as e:
            print(e)
    # 拿到eleven时候再去请求评论
    return eleven

def request_oceanball(cb, t):
    url_ocean = 'https://hotels.ctrip.com/domestic/cas/oceanball?callback={0}&_={1}'.format(cb, t)
    html = requests.get(url_ocean, headers=headers_ocean)
    return html.content.decode('utf-8')
def read_cookie(file):
    f = open(file,"r")   #设置文件对象
    str = f.read()     #将txt文件的所有内容读入到字符串str中
    f.close()
    return str;

def main(argv):
    all_hotel_month_lowest_price=pacoEnemyFutrueOnCtrip();
    writeEnemyFutrueData(all_hotel_month_lowest_price);
def queyEnemyPrice(startDate,endDate,hotelId,hotelName,cookie):
    referurl="https://hotels.ctrip.com/hotel/";
    url="https://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx";
    referurl=referurl+hotelId+".html";
    headers_ocean['referer']=referurl;
    headers['referer']=referurl;
    headers['cookie']=cookie;
    encodeHotel=quote(hotelName);
    enemyUrl=url+encodeHotel+"#ctm_ref=hod_hp_sb_lst";
    print(enemyUrl);
    #设置请求参数
    eleven=main_logic(hotelId);
    params = {
        'psid':"",
        'MasterHotelID': hotelId,
        'hotel': hotelId,
        'EDM':'F',
        'roomId':'',
        'IncludeRoom':'',
        'city':'32',
        'showspothotel':'T',
        'supplier':'',
        'IsDecoupleSpotHotelAndGroup': 'F',
        'contrast': '0',
        'brand': '0',
        'startDate': startDate.strftime('%Y-%m-%d'),
        'depDate': endDate.strftime('%Y-%m-%d'),
        'IsFlash': 'F',
        'RequestTravelMoney': 'F',
        'hsids': '',
        'IsJustConfirm': '',
        'contyped': '0',
        'priceInfo': '-1',
        'equip': '',
        'filter': '',
        'productcode': '',
        'couponList': '',
        'abForHuaZhu':'',
        'defaultLoad': 'T',
        'esfiltertag':'',
        'estagid': '',
        'Currency': 'RMB',
        'Exchange': '1',
        'minRoomId': '',
        'maskDiscount': '0',
        'TmFromList': 'F',
        'th': '202',
        'RoomGuestCount': '1,1,0',
        'eleven': eleven,
        'callback': get_callback(),
        '_': int(time.time()*1000)}
    #html = httpCall(url,"GET",params, headers)
    html = requests.get(url, headers=headers, params=params)
    content=html.content.decode('utf-8');
    data=json.loads(content);
    result_html=decrypt(data['ComplexHtml'],data['ASYS']);
    soup = BeautifulSoup(result_html, "html5lib");
    priceList = soup.findAll("td",{"class":"child_name J_Col_RoomName"});
    prices=[]
    for priceAttr in priceList:
        price=priceAttr.get("data-price");
        prices.append(price);
    print(prices);
    prices=list(map(int,prices));
    print(prices);
    return str(prices[0]);
def pacoEnemyFutrueOnCtrip():
    enemy=["丽柏国际|428643","嘉逸国际酒店|431937","桔子酒店岗顶店|1732435","总统大酒店天河岗顶店|392492","广州来福广武酒店|392493","柏高酒店体育西店|2981735","柏高酒店太古汇店|431298","柏高酒店龙口西店|449125","广州大华酒店|441047"]
    cookie_file=os.path.join(sys.path[0],"cookie.txt");
    cookie=read_cookie(cookie_file);
    all_hotel_month_lowest_price=[];
    for hotel_nameid in enemy:
        today = datetime.datetime.now();
        for i in range(30):            
            startDay=today;
            endDay=today+datetime.timedelta(days=1);
            [name,id]=hotel_nameid.split("|");
            hotel_month_lowest_price=[];
            price=queyEnemyPrice(startDay,endDay,id,name,cookie);
            hotel_month_lowest_price=[name,startDay.strftime('%Y-%m-%d'),price];
            print(hotel_month_lowest_price);
            all_hotel_month_lowest_price.append(hotel_month_lowest_price);
            today=endDay;
    return all_hotel_month_lowest_price;
        
def decrypt(n, t):
    c = ""
    for i in n:
        try:
            o = t[ord(i) - 21760];
        except:
            o = "";
        c = c + o
    return c
def createFutrueExcel(excel_file):
    f = xlwt.Workbook() #创建工作簿
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    sheet1.write(0, 0, '酒店名称')
    sheet1.write(0, 1, '日期')
    sheet1.write(0, 2, '最低价格')
    sheet1.write(0, 3, '是否可订')
    f.save(excel_file)
def writeEnemyFutrueData(prices):
    folder=os.path.join(sys.path[0],"tendency")
    if os.path.exists(folder):
        print("folder exists")
    else:
        os.makedirs(folder)
    excel_file=os.path.join(folder,"龙口西店周边未来30天价格详情.xls")
    if os.path.exists(excel_file):
        print("file exists")
    else:
        createFutrueExcel(excel_file)
    r_xls = open_workbook(excel_file)
    row = r_xls.sheets()[0].nrows
    excel = copy(r_xls)
    table = excel.get_sheet(0)
    for i,v in enumerate(prices):
        print(prices[i][0]);
        table.write(row, 0, prices[i][0]) #括号内分别为行数、列数、内容
        table.write(row, 1, prices[i][1])
        table.write(row, 2, prices[i][2])
        row=row+1
    excel.save(excel_file) # 保存并覆盖文件
if __name__ == '__main__':
    main(sys.argv)
