import requests
import lxml.html as HTML
import sys
import time
import gevent
from gevent import monkey
monkey.patch_all()

def get_data(num):
	t1 = time.time()
	res = requests.get(url='http://grri94kmi4.app.tianmaying.com/songs',params={'page':num})
	if res.status_code == 200:
		print('http://grri94kmi4.app.tianmaying.com/songs'+str(num)+' : '+'url open success'+'  time use: '+ str(time.time()-t1))
	html = HTML.fromstring(res.content)
	trs = html.xpath('//tbody/tr')
	data = []
	for tr in trs:
		s = {}
		s['name'] = tr.xpath('./td/a/text()')[0]
		s['url'] = tr.xpath('./td/a/@href')[0]
		s['id'] = s['url'][30:]
		s['comment'] = tr.xpath('./td[last()]/text()')[0]
		data.append(s) 
	return data
if __name__ == '__main__':
	total = time.time()
	task = []
	for num in range(int(sys.argv[1]),int(sys.argv[2])):
		task.append(gevent.spawn(get_data,num))
	gevent.joinall(task)
	for t in task:
		print(t.value)

	print('total time use :', time.time()-total)
