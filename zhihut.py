# -*- coding: utf-8 -*-
import requests
import re
import json
from urllib import parse, request
from PIL import Image
import os, time
from bs4 import BeautifulSoup
import http.cookiejar
proxies = {"https": "http://10.168.57.241:8088","http": "http://10.168.57.241:8088"}
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
agent1 = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
hds={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Referer':'https://www.zhihu.com/', 'Host':'www.zhihu.com', 'X-Requested-With':'XMLHttpRequest'}
session = requests.Session()
session.cookies = http.cookiejar.LWPCookieJar("cookie")
try:
    session.cookies.load(ignore_discard=True)
except IOError:
    print('Cookie未加载！')

def get_xsrf():
	s = requests.Session()
	soup = BeautifulSoup(s.get('https://www.zhihu.com/',headers=hds).text, "html.parser")
	xsrf = soup.find(type='hidden')['value']
	return xsrf

def get_xsrf_follow():
	hds1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Referer':'https://www.zhihu.com/question/22591304/followers','host':'www.zhihu.com','Origin':'https://www.zhihu.com','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest','Content-Length':'17','Accept-Encoding':'gzip,deflate,br','Accept-Language':'zh-CN,zh;q=0.8','Connection':'keep-alive','X-Xsrftoken':'b7181999-467d-4441-9be7-090f8acfa0de'}
	s = requests.Session()
	soup = BeautifulSoup(s.get('https://www.zhihu.com/question/22591304/followers',headers=hds1).text, "html.parser")
	xsrf = soup.find(type='hidden')['value']
	return xsrf

def login():
	loginurl = 'https://www.zhihu.com/login/phone_num'
	data={'_xsrf':get_xsrf(),'phone_num': 'X', 'password': 'X', 'remember_me': 'true'}
	#result = session.post(url=loginurl, data=data, headers=hds)
	#print (result.status_code)
	#session.cookies.save(ignore_discard=True, ignore_expires=True)
	#print (result.text)
	#print (json.loads(result.text)["msg"])
	#if json.loads(result.text)["r"] == 1:
	#获取验证码数据
	data['captcha'] = get_captcha()
	print (data)
	result = session.post(url=loginurl, data=data, headers=hds)
	#print (json.loads(result.text)["msg"])
	print (result.text)
	session.cookies.save(ignore_discard=True, ignore_expires=True)

def get_captcha():
	randomtime = str(int(time.time() * 1000))
	captcha_url = 'https://www.zhihu.com/captcha.gif?r='+randomtime+"&type=login"
	response = session.get(captcha_url, headers=hds)
	with open('cptcha.gif', 'wb') as f:
		f.write(response.content)
	im = Image.open('cptcha.gif')
	im.show()
	captcha = input('请输入验证码：')
	print (captcha)
	return captcha

def get_captcha_cn():
	randomtime = str(int(time.time() * 1000))
	captcha_url = 'https://www.zhihu.com/captcha.gif?r='+randomtime+"&type=login&lang=cn"
	response = session.get(captcha_url, headers=hds)
	with open('cptcha.gif', 'wb') as f:
		f.write(response.content)
	im = Image.open('cptcha.gif')
	im.show()
	i = input('请输入第一个倒立的汉字序号：')
	j = input('请输入第二个倒立的汉字序号：')
	points_data = [[12.95,14.969999999999998],[36.1,16.009999999999998],[57.16,24.44],[84.52,19.17],[108.72,28.64],[132.95,24.44],[151.89,23.380000000000002]]
	points_reverse_A = points_data[int(i)-1]
	points_reverse_B = points_data[int(j)-1]
	points_reverse = [points_reverse_A,points_reverse_B]
	captcha = {"img_size":[200,44],"input_points":points_reverse}
	print(captcha)
	return captcha

def isLogin():
	testloginurl = "https://www.zhihu.com/question/22591304/followers"
	login_code_status = session.get(url=testloginurl, headers=hds, allow_redirects=False).status_code
	if login_code_status == 200:
		return True
	else:
		return False

def get_settings():
	testloginurl = "https://www.zhihu.com/settings/profile"
	login_code = session.get(url=testloginurl, headers=hds, allow_redirects=False)
	print (login_code.text)

def get_photo():
	photourl="https://www.zhihu.com/question/22591304/followers"
	#cookies = {'_zap':'428a66f8-3337-4faf-aaed-d20f6be4c2ec','d_c0':'"AIDCEHgOVAyPTha6QTvVMOUVucqWUaeGwcs=|1504579367"','q_c1':'a1763451db1049249155b5ed64428800|1507876706000|1501233009000','q_c1':'a1763451db1049249155b5ed64428800|1506755186000|1501233009000','aliyungf_tc':'AQAAAFO6tmhrbQsAsgPK2gwTyzszdHnS','_xsrf':'b7181999-467d-4441-9be7-090f8acfa0de','__utma':'51854390.360216818.1509519765.1509519765.1509956841.2','__utmc':'51854390','__utmb':'51854390.0.10.1509956841' '__utmz':'51854390.1509519765.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','__utmv':'51854390.100--|2=registration_date=20150620=1^3=entry_date=20150620=1','z_c0':'Mi4xSjdMS0FRQUFBQUFBZ01JUWVBNVVEQmNBQUFCaEFsVk4yYm5tV2dDaGhwRUh5MmZfczRZQ0xmbkhfczQtUlJSUHR3|1509518297|d922ca8d654a8c3021fa70f462be8af808a978e6','r_cap_id':'"ZTE2YTQ4MmM2MTZjNDY0MmJjZWI1NmM4MWNkMThiY2M=|1509518285|0b9b902fdee309db5348af64925b1a14dc6e6426"','cap_id':'"YzA4Y2FlNDkyOTBiNDMyY2E0NTkwYTdhY2JjY2NkZDA=|1509518285|147c2b5a1645bec65b7960b7311e0aafc48a12fa"'}
	hds1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Referer':'https://www.zhihu.com/question/22591304/followers','host':'www.zhihu.com','Origin':'https://www.zhihu.com','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest','Content-Length':'17','Accept-Encoding':'gzip,deflate,br','Accept-Language':'zh-CN,zh;q=0.8','Connection':'keep-alive','X-Xsrftoken':'b7181999-467d-4441-9be7-090f8acfa0de'}
	#photo_page_static=session.get(url=photourl,cookies=cookies,headers=hds).text
	data1 = {'start':'0','offset':'20'}
	#photo_page = session.post(url=photourl, data=data1, headers=hds).text
	photo_page = session.get(url=photourl,headers=hds).text
	print(photo_page)
	#dizhi = re.compile(r'<img src="(.*)" class')
	#imgs = dizhi.findall(photo_page_static)
	#print (imgs)
	return

def get_photo_post():
	photourl="https://www.zhihu.com/question/22591304/followers"
	#cookies ={'_zap':'428a66f8-3337-4faf-aaed-d20f6be4c2ec','d_c0':'"AIDCEHgOVAyPTha6QTvVMOUVucqWUaeGwcs=|1504579367"','q_c1':'a1763451db1049249155b5ed64428800|1507876706000|1501233009000','q_c1':'a1763451db1049249155b5ed64428800|1506755186000|1501233009000','aliyungf_tc':'AQAAAFO6tmhrbQsAsgPK2gwTyzszdHnS','_xsrf':'b7181999-467d-4441-9be7-090f8acfa0de','__utma':'51854390.360216818.1509519765.1509519765.1509956841.2','__utmc':'51854390','__utmb':'51854390.0.10.1509956841' '__utmz':'51854390.1509519765.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','__utmv':'51854390.100--|2=registration_date=20150620=1^3=entry_date=20150620=1','z_c0':'Mi4xSjdMS0FRQUFBQUFBZ01JUWVBNVVEQmNBQUFCaEFsVk4yYm5tV2dDaGhwRUh5MmZfczRZQ0xmbkhfczQtUlJSUHR3|1509518297|d922ca8d654a8c3021fa70f462be8af808a978e6','r_cap_id':'"ZTE2YTQ4MmM2MTZjNDY0MmJjZWI1NmM4MWNkMThiY2M=|1509518285|0b9b902fdee309db5348af64925b1a14dc6e6426"','cap_id':'"YzA4Y2FlNDkyOTBiNDMyY2E0NTkwYTdhY2JjY2NkZDA=|1509518285|147c2b5a1645bec65b7960b7311e0aafc48a12fa"'}
	hds1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Referer':'https://www.zhihu.com/question/22591304/followers','host':'www.zhihu.com','Origin':'https://www.zhihu.com','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Connection':'keep-alive','X-Requested-With':'XMLHttpRequest','Content-Length':'17','Accept-Encoding':'gzip,deflate,br','Accept-Language':'zh-CN,zh;q=0.8','Connection':'keep-alive','X-Xsrftoken':'37fe0cf3-76fc-4a60-91ec-64bc2bd62f88','Cookie':'_zap=428a66f8-3337-4faf-aaed-d20f6be4c2ec; d_c0="AIDCEHgOVAyPTha6QTvVMOUVucqWUaeGwcs=|1504579367"; q_c1=a1763451db1049249155b5ed64428800|1506755186000|1501233009000; q_c1=a1763451db1049249155b5ed64428800|1507876706000|1501233009000; aliyungf_tc=AQAAAEgNcHhCKgkAsgPK2pdobF4AsElE; r_cap_id="N2RmNTIwY2NiOTFkNDEzZTgwNTZhNmMwOTdhZmI1MzY=|1510042250|1ebd58d2cfeefb2e803357c67f232c8b90d7f7d7"; cap_id="YTk1ZGJjYjZlN2U0NDY1YWE4M2NjMmQ4ZGY4MGY4ZmU=|1510042250|28ae730993949ad574d35e34e7cbebb615eb0f0b"; _xsrf=37fe0cf3-76fc-4a60-91ec-64bc2bd62f88; z_c0=Mi4xSjdMS0FRQUFBQUFBZ01JUWVBNVVEQmNBQUFCaEFsVk40TG51V2dCLWpkSUhpTkJVMzY2TkhlWEVnQVhIV1NUV2ZR|1510042592|7600bcc3afd7ffba044e06d00cfb44dd613fb005; __utma=51854390.360216818.1509519765.1510021607.1510042262.5; __utmb=51854390.0.10.1510042262; __utmc=51854390; __utmz=51854390.1509519765.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20150620=1^3=entry_date=20150620=1'}
	hds2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Referer':'https://www.zhihu.com/question/22591304/followers','host':'www.zhihu.com','X-Xsrftoken':'37fe0cf3-76fc-4a60-91ec-64bc2bd62f88','Cookie':'_zap=428a66f8-3337-4faf-aaed-d20f6be4c2ec; d_c0="AIDCEHgOVAyPTha6QTvVMOUVucqWUaeGwcs=|1504579367"; q_c1=a1763451db1049249155b5ed64428800|1506755186000|1501233009000; q_c1=a1763451db1049249155b5ed64428800|1507876706000|1501233009000; aliyungf_tc=AQAAAEgNcHhCKgkAsgPK2pdobF4AsElE; r_cap_id="N2RmNTIwY2NiOTFkNDEzZTgwNTZhNmMwOTdhZmI1MzY=|1510042250|1ebd58d2cfeefb2e803357c67f232c8b90d7f7d7"; cap_id="YTk1ZGJjYjZlN2U0NDY1YWE4M2NjMmQ4ZGY4MGY4ZmU=|1510042250|28ae730993949ad574d35e34e7cbebb615eb0f0b"; _xsrf=37fe0cf3-76fc-4a60-91ec-64bc2bd62f88; z_c0=Mi4xSjdMS0FRQUFBQUFBZ01JUWVBNVVEQmNBQUFCaEFsVk40TG51V2dCLWpkSUhpTkJVMzY2TkhlWEVnQVhIV1NUV2ZR|1510042592|7600bcc3afd7ffba044e06d00cfb44dd613fb005; __utma=51854390.360216818.1509519765.1510021607.1510042262.5; __utmb=51854390.0.10.1510042262; __utmc=51854390; __utmz=51854390.1509519765.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20150620=1^3=entry_date=20150620=1'}
	#photo_page_static=session.get(url=photourl,cookies=cookies,headers=hds).text
	data1 = {'start':'0','offset':'20'}
	#photo_page_static = session.post(url=photourl, data=data1, headers=hds).text
	photo_page_static = session.get(url=photourl,headers=hds).text
	print(photo_page_static)
	dizhi = re.compile(r'<img src="(.*)" class')
	imgs = dizhi.findall(photo_page_static)
	print (imgs)
	print (len(imgs))
	return

if __name__ == '__main__':
	if isLogin():
		print('you have logined')
		#get_photo()
		get_photo_post()
	else:
		print('you don\'t logined, you are loging now...')
		login()
		#get_photo()
		#get_photo_post()
#print(get_xsrf())
