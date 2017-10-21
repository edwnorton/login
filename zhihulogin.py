import requests
import json
from urllib import parse, request
from PIL import Image
import os, time
from bs4 import BeautifulSoup
import http.cookiejar
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
	soup = BeautifulSoup(s.get('https://www.zhihu.com/#signin',headers=hds).text, "html.parser")
	xsrf = soup.find(type='hidden')['value']
	return xsrf

def login():
	loginurl = 'https://www.zhihu.com/login/email'
	data={'_xsrf':get_xsrf(),'email': 'xxx', 'password': 'xxx', 'remember_me': 'true'}
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
	print (json.loads(result.text)["msg"])
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
	testloginurl = "https://www.zhihu.com/settings/profile"
	login_code_status = session.get(url=testloginurl, headers=hds, allow_redirects=False).status_code
	if login_code_status == 200:
		return True
	else:
		return False

def get_settings():
	testloginurl = "https://www.zhihu.com/settings/profile"
	login_code = session.get(url=testloginurl, headers=hds, allow_redirects=False)
	print (login_code.text)

if __name__ == '__main__':
	if isLogin():
		print('you have logined')
		get_settings()
	else:
		login()
#print(get_xsrf())
