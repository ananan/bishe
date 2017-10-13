import requests
import lxml.html as HTML
import sys
import time
from queue import Queue
import dbcon

class songs:
	def __init__(self):
		try:
			self.db = dbcon.conn()
			print('connected to mysql...')
		except Exception as e:
			print('can not connecting to mysql: ',e)
		self.cursor = self.db.cursor()
		self.cursor.execute("set character_set_client=utf8")
		self.cursor.execute("set character_set_connection=utf8")
		self.cursor.execute("set character_set_results=utf8")
	def url_que(self):
		que = Queue()
		for page in range(int(sys.argv[1]),int(sys.argv[2])):
			url = 'http://grri94kmi4.app.tianmaying.com/songs?page='+str(page)
			que.put(url)
		return que

	def get_data(self,url):
		try:
			res = requests.get(url)
			return res
		except Exception as e:
			print("Error while getting url: ",e)

	def parse(self,res):
		html = HTML.fromstring(res.content)
		try:
			trs = html.xpath('//tbody/tr')
			for tr in trs:
				s = {}
				s['name'] = tr.xpath('./td/a/text()')[0]
				s['url'] = tr.xpath('./td/a/@href')[0]
				s['id'] = s['url'][30:]
				s['comment'] = tr.xpath('./td[last()]/text()')[0]
				yield s
		except Exception as e:
			print("Error while parse HTML: ",e)

	def save_data(self,s):
		sql = '''insert into songs(songs_id,songs_name,songs_url,songs_comment) value({sid},"{name}",'{url}',{comment})'''
		new_sql = sql.format(sid=s['id'],name=s['name'],url=s['url'],comment=s['comment'])
		try:
			self.cursor.execute(new_sql)
			self.cursor.execute('commit')
		except Exception as e:
			print('Error while insert into database: ', e)

if __name__ == '__main__':
	record = 0
	start = time.time()
	peter = songs()
	url_queue = peter.url_que()
	failed_url = []
	while True:
		if url_queue.empty():
			print('----*__*-------all pages has been finished !!----*__*---------')
			break
		else:
			st = time.time()
			url = url_queue.get()
			res = peter.get_data(url)
			if res.status_code == 200:
				for s in peter.parse(res):
					peter.save_data(s)
					record+=1
				print(url+"----------- process ok ! -------- time use: "+str(time.time()-st))
				print('---------- {} urls left in the Queue -----------'.format(url_queue.qsize()))
			elif res.status_code == 504:
				url_queue.put(url)
				print(url+"--------- timeout error, try again later ! -------time use: "+str(time.time()-st))
				print('---------- {} urls left in the Queue ----------'.format(url_queue.qsize()))
			else:
				print(url+"-----------other error: "+str(res.status_code))
				failed_url.append(url)
	peter.cursor.close()
	peter.db.close()	
	print('The number inserted is :',record)
	print('Time use: ',time.time()-start)
	print(failed_url)
	print('finished timestamp: ',time.localtime(time.time()))
