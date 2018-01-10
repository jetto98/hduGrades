import hashlib,sys,getpass
from http.cookiejar import LWPCookieJar as Cookie
import requests
from bs4 import BeautifulSoup
from functools import partial
bs = partial(BeautifulSoup,features='html.parser')
baseURL="http://cas.hdu.edu.cn/cas/login"
def xuke_login(userName,password):
    s = requests.session()
    cookiefile = 'xkcookies.txt'
    s.cookies = Cookie(cookiefile)
    s.headers['Referer']=baseURL
    try:
        r = s.get(baseURL,timeout=5)
    except Exception:
        print("请求超时")
        sys.exit(1)
    data={
        'encodedService':'http://jxglteacher.hdu.edu.cn/default.aspx',
        'service':'http://jxglteacher.hdu.edu.cn/default.aspx',
        'serviceName':'null',
        'loginErrCnt':'0',
        'username':userName,
        'password':hashlib.md5(password.encode()).hexdigest(),
        'lt':bs(r.text).select('input[name="lt"]')[0]['value'],
    }
    try:
        r=s.post(baseURL,data=data,timeout=1)
        s.get(bs(r.text).select('a')[0]['href'],timeout=1)
        r=s.get('http://jxglteacher.hdu.edu.cn/xs_main.aspx?xh=%s' % userName)
        s.cookies.save(ignore_discard=True, ignore_expires=True)
    except Exception:
        print("密码错误,请重新登录")
        sys.exit(1)
    with open(".username","w") as f:
        f.write(userName)
if __name__=="__main__":
    print("\t\t登录数字杭电选课系统")
    userName=input("数字杭电账号:")
    password=getpass.getpass("数字杭电密码(不显示位数):")
    xuke_login(userName,password)
    print("登录成功")
