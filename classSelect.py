import time
import requests
from http.cookiejar import LWPCookieJar as Cookie
import requests,re
from bs4 import BeautifulSoup
from functools import partial
import json
import urllib.parse as parse
bs = partial(BeautifulSoup,features='html.parser')
info_data = None
data={}
s=None
params=None
def loadJson():
    global info_data
    with open("data.json","r") as f:
        info_data=json.loads(f.read())

def load_cookies():
    global s
    s=requests.session()
    s.cookies = Cookie()			
    s.cookies.load('xkcookies.txt',ignore_discard=True, ignore_expires=True)
def set_params():
    global params
    params = parse.urlencode(
            {
                "gnmkdm":"N121113",
                "xh":info_data["id"],
                "xm":info_data["name"]
            },encoding="gbk")
def set_form(r):
    data = {
        "__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        "__LASTFOCUS":"",
        "__VIEWSTATE":bs(r.text).select('input[name="__VIEWSTATE"]')[0]['value'],
        "__EVENTVALIDATION":bs(r.text).select('input[name="__EVENTVALIDATION"]')[0]['value'],
        "ddl_kcxz":"",
        "ddl_ywyl":"有".encode("gbk"),
        "ddl_kcgs":"通识选修一般课".encode("gbk"),
        "ddl_xqbs":"1",
        "ddl_sksj":"",
        "TextBox1":"",
        "txtYz":"",
        "hidXNXQ":"2017-20182",
    }
    return data
def get_code():
    with open("123.gif","wb" ) as f:
        f.write(s.get("http://jxglteacher.hdu.edu.cn/CheckCode.aspx").content)

if __name__ == "__main__":
    now=time.time()
    loadJson()
    load_cookies()
    set_params()
    r=s.get("http://jxglteacher.hdu.edu.cn/xf_xsqxxxk.aspx?%s" % params,headers={"Referer":"http://jxglteacher.hdu.edu.cn/xs_main.aspx?xh=%s"%info_data["id"]})
    data=set_form(r)
    r=s.post("http://jxglteacher.hdu.edu.cn/xf_xsqxxxk.aspx?%s" % params,data=data,headers={"Referer":"http://jxglteacher.hdu.edu.cn/xf_xsqxxxk.aspx?%s" % params})
    get_code()
    data=set_form(r) 
    data["Button1"]="  提交  ".encode("gbk")
    data["txtYz"]=input("xx:")
    for d in info_data["class"]:
        data[d]="on"
    r=s.post("http://jxglteacher.hdu.edu.cn/xf_xsqxxxk.aspx?%s" % params,data=data,headers={"Referer":"http://jxglteacher.hdu.edu.cn/xf_xsqxxxk.aspx?%s" % params})
    print(r.text)
    print(time.time()-now) 
    


