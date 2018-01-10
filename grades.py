import hashlib,os,sys
import datetime

from http.cookiejar import LWPCookieJar as Cookie
import requests
from bs4 import BeautifulSoup
from functools import partial
bs = partial(BeautifulSoup,features='html.parser')

from pyexcel_xls import save_data
from collections import OrderedDict

grades=[['学年','学期','课程代码','课程名称','课程性质','课程归属','学分','成绩','补考成绩','是否重修','开课学院','备注','补考备注']]
s=None
def load_cookies():
    global s
    s=requests.session()
    s.cookies = Cookie()			
    s.cookies.load('xkcookies.txt',ignore_discard=True, ignore_expires=True)
def isnumber(x):
    x=x.string
    if x.isdigit():
        return int(x)
    try:
        fx=float(x)
        return fx
    except Exception:
        return x
def classinfo(html):
    data=html.find_all('td')
    return list(map(isnumber,data))
def getGrades(userName,xn,xq):
    global s
    data={
        '__EVENTTARGET' : '',
        '__EVENTARGUMENT' : '',
        '__LASTFOCUS' : '',
        'ddlxn' : xn,
        'ddlxq' : xq,
    }
    s.headers['Referer'] = 'http://jxgl.hdu.edu.cn/xs_main.aspx?xh={0}'.format(userName)
    try:
        r=s.get('http://jxgl.hdu.edu.cn/xscjcx_dq.aspx?xh={0}&xm=%C2%C0%EA%BB%C1%D9&gnmkdm=N121605'.format(userName),timeout=2)
        for put in bs(r.text).find_all('input'):
            data[put['name']] = put['value']
        r=s.post('http://jxgl.hdu.edu.cn/xscjcx_dq.aspx?xh={0}&xm=%u5415%u660a%u4e34&gnmkdm=N121605'.format(userName),data=data,timeout=2)
    except Exception:
        print("cookies过期,请重新登录")
        sys.exit(1)
    try:    
        for r in bs(r.text).find_all('tr')[4:]:
            grades.append(classinfo(r))
    except Exception as e:
        print(e)
        print("emmm...挂了")
        sys.exit(1)
def get_xq_xns(userName):
    qn=[]
    try:
        start_year=int("20%s"%userName[:2])
        now_year=int(datetime.datetime.now().year)
        for year in range(start_year,now_year):
            qn.append(("{}-{}".format(year,year+1),'1'))
            if year<now_year:
                qn.append(("{}-{}".format(year,year+1),'2'))
    except Exception:
        print("学号格式有误")
        sys.exit(1)
    return qn
def save_to_xls():
    od=OrderedDict()
    if len(grades)==1:
        print("爬取失败,请重新登录")
        sys.exit(1)
    od.update({'成绩单1':grades})
    save_data('成绩单.xls',od)

if __name__=="__main__":
    print("开始爬取")
    with open(".username","r") as f:
        userName=f.read()
        if userName!="":
            load_cookies()
            for (xn,xq) in get_xq_xns(userName):
                getGrades(userName,xn,xq)
            save_to_xls()
            print("爬取结束")
        else:
            print("请先登录")
            sys.exit(1)
paramters = urllib.urlencode({
						'xh': "123123", 
						'xm': "吕昊临".decode('utf-8').encode('gbk'),
						'gnmkdm': 'N121113'})