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


def main(argv):
    pacoEnemyOnCtrip();
def pacoEnemyOnCtrip():
    enemy=["丽柏国际","嘉逸国际酒店","桔子酒店岗顶店","总统大酒店天河岗顶店","广州来福广武酒店","柏高酒店体育西店","柏高酒店太古汇店","柏高酒店龙口西店","广州大华酒店"]
#    enemy=["丽柏国际"]
    url="https://hotels.ctrip.com/hotel/guangzhou32/k1";
    priceXPath=".hotel_new_list J_HotelListBaseCell .hotel_item .hotel_price_icon .";
    priceXpathEnd=" .hotel_price . "
    prices = [];
    for hotel in enemy:
        enemyUrl="";
#        print(hotel);
        encodeHotel=quote(hotel);
        enemyUrl=url+encodeHotel;
        #print('cityName=' + cityName + ',cityId='+ cityId);
        #设置请求参数
        keyword = hotel;
        today = datetime.datetime.now();
        startDay=today;
        endDay=today+datetime.timedelta(days=1);
        param = {'page':1};
        param['__VIEWSTATEGENERATOR'] = 'DB1FBB6D';
        param['cityName']='广州';
        param['StartTime']=startDay.strftime('%Y-%m-%d');
        param['DepTime']=endDay.strftime('%Y-%m-%d');
        param['RoomGuestCount']='1,1,0';
        param['txtkeyword']=hotel;
        param['Resource']='';
        param['Room']='';
        param['Paymentterm']='';
        param['BRev']='';
        param['Minstate']='';
        param['PromoteType']='';
        param['PromoteDate']='';
        param['operationtype']='NEWHOTELORDER';
        param['PromoteStartDate']='';
        param['PromoteEndDate']='';
        param['OrderID']='';
        param['RoomNum']='0';
        param['IsOnlyAirHotel']='F';
        param['cityId']='32';
        param['cityPY']='guangzhou';
        param['cityCode']='020';
        param['cityLat']='23.143407';
        param['cityLng']='113.331577';
        param['cityName']='广州';
        param['positionArea']='';
        param['positionId']='';
        param['hotelposition']='0,0';
        param['keyword']=hotel;
        param['hotelId']='';
        param['htlPageView']='0';
        param['hotelType']='F';
        param['hasPKGHotel']='F';
        param['requestTravelMoney']='F';
        param['isusergiftcard']='F';
        param['useFG']='F';
        param['HotelEquipment']='';
        param['priceRange']='-2';
        param['hotelBrandId']='';
        param['RoomNum']='';
        param['promotion']='F';
        param['prepay']='F';
        param['IsCanReserve']='F';
        param['OrderBy']='';
        param['OrderType']='';
        param['k1']='';
        param['k2']='';
        param['CorpPayType']='';
        param['viewType']='';
        param['checkIn']=startDay.strftime('%Y-%m-%d');
        param['checkOut']=endDay.strftime('%Y-%m-%d');
        param['DealSale']='';
        param['ulogin']='';
        param['hidTestLat']='0|0';
        param['AllHotelIds']='428643,441047,6672193,431937,392495,392493,392492,449125,396594,1233759';
        param['psid']='';
        param['isfromlist']='T';
        param['ubt_price_key']='htl_search_result_promotion';
        param['showwindow']='';
        param['defaultcoupon']='';
        param['isHuaZhu']='False';
        param['hotelPriceLow']='';
        param['unBookHotelTraceCode']='';
        param['showTipFlg']='';
        param['traceAdContextId']='';
        param['allianceid']='0';
        param['sid']='0';
        param['pyramidHotels']='';
#        print(param);
        html_doc = urlopen(enemyUrl);
        soup = BeautifulSoup(html_doc, "html5lib", from_encoding='utf-8');
        hotelList = soup.findAll("div",{"class":"hotel_new_list J_HotelListBaseCell"});
        for hotelInfo in hotelList:
            data=hotelInfo.get("data-maidian");
            infos=data.split(",");
            id=0;
            price="";
            editdate="";
            sale="";
            if len(infos)==1:
                continue;
            for i,v in enumerate(infos):
                if i==0:
                   id=v;
                elif i==4:
                   price=v;
                elif i==5:
                   editdate=v;
            saleOut=hotelInfo.findAll("div",{"class":"sale_out"});
            print(saleOut);
            if saleOut:
                sale="已订完";
            else:
                sale="可预订";
            hotelPrice=[hotel,price,editdate,sale,today.strftime('%Y-%m-%d %H')];
            prices.append(hotelPrice);
    writeEnemyTendency(prices);
def createTendencyExcel(excel_file):
    f = xlwt.Workbook() #创建工作簿
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    title=['酒店名称','最低价格','更新时间','是否可订']
    sheet1.write(0, 0, '酒店名称')
    sheet1.write(0, 1, '最低价格')
    sheet1.write(0, 2, '更新时间')
    sheet1.write(0, 3, '是否可订')
    f.save(excel_file)
    print("create excel file:"+excel_file);
def writeEnemyTendency(prices):
    folder=os.path.join(sys.path[0],"tendency")
    if os.path.exists(folder):
        print("folder exists")
    else:
        os.makedirs(folder)
    excel_file=os.path.join(folder,"龙口西店周边当天实时房价变动.xls")
    if os.path.exists(excel_file):
        print("file exists")
    else:
        createTendencyExcel(excel_file)
    r_xls = open_workbook(excel_file)
    row = r_xls.sheets()[0].nrows
    excel = copy(r_xls)
    table = excel.get_sheet(0)
    for i,v in enumerate(prices):
        print(prices[i][0]);
        table.write(row, 0, prices[i][0]) #括号内分别为行数、列数、内容
        table.write(row, 1, prices[i][1])
        table.write(row, 2, prices[i][4])
        table.write(row, 3, prices[i][3])
        row=row+1
    excel.save(excel_file) # 保存并覆盖文件
if __name__ == '__main__':
    main(sys.argv)
