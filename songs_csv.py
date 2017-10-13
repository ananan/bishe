import requests
import lxml.html as HTML
import sys
import time

def get_data(s,beg,end):
	for i in range(int(beg),int(end)):
#		url = 'http://grri94kmi4.app.tianmaying.com/songs?page='+str(i-1)
		url = 'http://grri94kmi4.app.tianmaying.com/songs'
		res = s.get(url = url,params={'page':i})
		if res.status_code == 200:
			print(url+str(i)+' : '+'url open success')
			yield res

def parse(res):
	html = HTML.fromstring(res.content)
	trs = html.xpath('//tbody/tr')
	for tr in trs:
		s = {}
		s['name'] = tr.xpath('./td/a/text()')[0]
		s['url'] = tr.xpath('./td/a/@href')[0]
		s['id'] = s['url'][30:]
		s['comment'] = tr.xpath('./td[last()]/text()')[0]
		yield s


if __name__ == '__main__':
	start = time.time()
	
	s = requests.session()
	for res in get_data(s,sys.argv[1],sys.argv[2]):
		for s in parse(res):
			print(s)
	print('Time use: ',time.time()-start)
