import requests
import lxml,time,os
from bs4 import BeautifulSoup as sb
from xlwt import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

book = Workbook(encoding = "utf-8")
table = book.add_sheet("test1")
'''table.write(0,0,'number')
table.write(0,1,'position')
table.write(0,2,'feedback')
table.write(0,3,'company')
table.write(0,4,'salary')
table.write(0,5,'address ')
table.write(0,6,"updatetime")
table.write(0,7,"details")'''

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}

for num in range(5):
	url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3%2B%E5%B9%BF%E5%B7%9E%2B%E4%B8%9C%E8%8E%9E&kw=python&p='+str(num)
	print url
	res = requests.get(url,headers = headers)
	html = sb(res.text,'lxml')
	zwmc = html.find_all('td',class_="zwmc")
	for i in range(1,len(zwmc)):
		page_url = zwmc[i].a.get("href")
		print page_url
		page_res = requests.get(page_url,headers = headers)
		page_html = sb(page_res.text,'lxml')
		divs = page_html.find("div",class_="terminalpage-main clearfix")
		texts = divs.div.div.text.strip()
		print texts
		table.write(num*len(zwmc)+i,1,texts)


book.save('result1.xls')