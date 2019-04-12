import requests
import lxml.html as HTML
import pymysql
import sys
import time
from multiprocessing.dummy import Pool
def get_data(page):
	url = 'http://grri94kmi4.app.tianmaying.com/songs?page='
	t1 = time.time()
	res = requests.get(url+str(page))
	if res.status_code == 200:
		print(url+str(page)+' : '+'url open success'+'  time use: '+ str(time.time()-t1))
		return res
	else:
		print(res)
		print(url+str(page)+'  url open failed !!')
		
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

def save_data(s):
	sql = '''insert into songs(songs_id,songs_name,songs_url,songs_comment) value({sid},"{name}",'{url}',{comment})'''.format(sid=s['id'],name=s['name'],url=s['url'],comment=s['comment'])
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	try:
		cursor.execute(sql)
	except Exception as e:
		print('raise exception :', e)

if __name__ == '__main__':
	record = 0
	start = time.time()
	# open the database
	db = pymysql.connect(host='localhost',user='root',passwd='alexwei',db='peter',charset='utf8')
	cursor = db.cursor()
	pages = list(range(int(sys.argv[1]),int(sys.argv[2])))
	pool = Pool()
	results = pool.map(get_data,pages)
	pool.close()
	pool.join()
	for res in results:
		if res:
			for s in parse(res):
				save_data(s)
				record+=1
				cursor.execute('commit')
		else:
			pass
	# close database
	db.close()	
	print('The number inserted is :',record)
	print('Time use: ',time.time()-start)
