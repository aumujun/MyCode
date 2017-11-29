import urllib.request
import http.cookiejar
import requests
import http.cookies

filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
rsp = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)
