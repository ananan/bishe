# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as sb
import os
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_weather():
	url = "http://tianqi.moji.com"
	res = requests.get(url)
	soup = sb(res.text,'html.parser')
	node1 = soup.find('div',class_="left")
	alert   = '空气质量指数为：'+node1.find('div',class_="wea_alert clearfix").text.strip()
	weather = '天气：'+ node1.find('div',class_="wea_weather clearfix").b.text+'，气温：'+node1.find('div',class_="wea_weather clearfix").em.text +'度'
	
	about   = node1.find('div',class_="wea_about clearfix").text.strip().replace('\n','，')
	tips    = node1.find('div',class_="wea_tips clearfix").text.strip().replace('\n','：')
	text = alert+ '，' +weather+ '，' +about+ '，' +tips 
	return text

def get_token():
	# get token
	data1 = {
			 "grant_type":"client_credentials",
			 "client_id":"k8jc8zaPeLUNeTC1HKGmwumA",
			 "client_secret":"VE8avSsFVIQfghTq2jgp9mfaP0W4p7i7"
			}
	token = requests.post(url="https://openapi.baidu.com/oauth/2.0/token",data=data1).json()["access_token"]
	return token

if __name__=='__main__':
	text = '起床啦！大懒虫起床啦！今天要上班呢，记得吃早餐喔！'+get_weather()+'接下来给宝宝放一首好听的歌吧！'
	print text
	token = get_token()
	# make audio url for mpg123 to read
	aud_url = "http://tsn.baidu.com/text2audio?tex={tex}&tok={tok}&lan=zh&cuid=192.168.12.183&ctp=1&lan=zh&spd={spd}&pit={pit}&vol={vol}&per={per}".format(tex=text,tok=token,spd=3,pit=6,vol=12,per=4)
	os.system("mpg123 '%s'" %(aud_url))
	# make music list
	base_url = "http://music.163.com/song/media/outer/url?id="
	music_id = [28815250,25718007,30780431]
	for m in music_id:
		music_url = base_url+str(m)+'.mp3'
		print music_url
		os.system("mpg123 '%s'"%(music_url))

