import requests
import os
import re
from bs4 import BeautifulSoup
import hashlib
from functools import partial
from http.cookiejar import LWPCookieJar as Cookie
bs = partial(BeautifulSoup,features="html.parser")
import time
headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}
def hdu_login(userName,password):
    s = requests.session()
    cookiefile = 'cookies.txt'
    s.cookies = Cookie(cookiefile)
    r = s.get('http://cas.hdu.edu.cn/cas/login',headers=headers)
    headers['Referer']='http://cas.hdu.edu.cn/cas/login'
    cookiefile = 'cookies.txt'
    data={
        'encodedService':'http://i.hdu.edu.cn/dcp/index.jsp',
        'service':'http://i.hdu.edu.cn/dcp/index.jsp',
        'serviceName':'null',
        'loginErrCnt':'0',
        'username':userName,
        'password':hashlib.md5(password.encode()).hexdigest(),
        'lt':bs(r.text).select('input[name="lt"]')[0]['value'],
    }
    r=s.post('http://cas.hdu.edu.cn/cas/login',headers=headers,data=data)
    s.get(bs(r.text).select('a')[0]['href'],headers=headers)
    r=s.get('http://i.hdu.edu.cn/dcp/forward.action?path=/portal/portal&p=wkHomePage',headers=headers)
    s.cookies.save(ignore_discard=True, ignore_expires=True)

hdu_login('15058220','LHL1210HH')