#coding:utf-8

import socket
import requests
from pyquery import PyQuery as pq
import time

CHROME = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
COOKIE = 'SINAGLOBAL=1356131259817.6301.1443526191405; _ga=GA1.2.1846915066.1443526092; lzstat_uv=16710466491215093168|2893156; myuid=5851235232; wvr=6; _s_tentry=login.sina.com.cn; Apache=9983387885149.568.1456549198468; ULV=1456549198496:31:5:4:9983387885149.568.1456549198468:1456326476255; PHPSESSID=r1or60rslukmj1pnl5lsqfshu2; USRHAWB=usrmdinst_23; WBStore=8b23cf4ec60a636c|undefined; login_sid_t=e49e97e841d0a749301e18e4cadc4867; SUS=SID-2417990255-1456644322-GZ-2gerd-408fc86bfe24d491784cc00d11a04482; SUE=es%3D8092931bf191128f7dbd3c448bd16c63%26ev%3Dv1%26es2%3Dc79d1f13e6ed51bd41a98b9f365223fd%26rs0%3DhS9xiwf99UCpRRKjg8Qs5EnSAL48iH7yGpbEMbS%252FE8LcCjvqK0FRZvA2CBavAYpoP%252FH8OmTB62XP6P%252F%252Fr9DWblrnuOQbiu2%252B2oqSRraRBL5y7And2UoUYJcz2C5FrZHzQvrCYYaARY5x49sTEhEgfJ2GX3E6iolzcT5WehKqPbs%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1456644322%26et%3D1456730722%26d%3Dc909%26i%3D4482%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D2417990255%26name%3Dwangjianan527%2540sina.cn%26nick%3D%25E5%2594%25A7%25E5%2594%25A7%26fmp%3D%26lcp%3D; SUB=_2A2571tCyDeRxGeRK6lUY-S7OzjmIHXVYokV6rDV8PUNbuNBeLW3wkW9LHeteQ748iU-4iZX0v3-kKMqGVX0-MQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFF-VJCV9M.0iF8geNEIDlb5JpX5K2t; SUHB=0TPkMaG9UqKFMk; ALF=1488180322; SSOLoginState=1456644322; un=wangjianan527@gmail.com; UOR=,,book.51cto.com; __utmt=1; lzstat_ss=3313736729_5_1456739325_2893156; __utma=63176942.1846915066.1443526092.1456572451.1456708704.37; __utmb=63176942.6.10.1456708704; __utmc=63176942; __utmz=63176942.1456144201.29.3.utmcsr=app.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/detail/4G3OlD'
baseurl = 'http://place.weibo.com/search?city=0021&prov=0&cat=&page=search&keyword={}&cat_name=&city_name=%E4%B8%8A%E6%B5%B7'


header = {'Connection': 'keep-alive', 'cookie': COOKIE, 'User-Agent': CHROME}

# 将点评上site的名字文件加载进内存，存在一个list中（后续这些sitename要query微博）
def load_malls(filename):
	bigmalls = []
	f = open(filename, 'r')
	for name in f:
		bigmalls.append(name.strip())
	f.close()
	return bigmalls

def load_data(filename):
	# 只适用于file中每一行数据是由","分隔的
	l = []
	with open(filename, 'r') as f:
		for line in f:
			data = line.split(',')[0].strip()
			l.append(data)
	return l

def query_weibo(url):
	while True:
		try:
			r = requests.get(url, headers= header).text
		except (socket.timeout, requests.exceptions.Timeout):  # socket.timeout
			print "timeout", url
		except requests.exceptions.ConnectionError:
			print "connection error", url
		else:
			break
	return r

def parse_page(r):
	import re
	# 每一页展示的所有query到的结果，都是写在文件中的一行
	page_str = '' # res存储的是所有的结果，翻页后的结果也写在res中

	# 如果存在任何搜索结果，都进行解析；如果不存在，直接返回''字符串
	if not pq(r)('.search_noresult'):
		for each in pq(r)('div.w_result')('li'):
			weibo = ''
			users = ''
			photos = ''
			name = pq(each)('dd.details')('p').eq(0).text()
			addr = pq(each)('dd.details')('p').eq(1).text()
			# 经纬度
			lat = pq(each)('div.w_vspii').attr('actlat')
			lon = pq(each)('div.w_vspii').attr('actlon')
			pos = (float(lat), float(lon))

			weibo_info = pq(each)('dd.details')('p').eq(2)('a').filter(lambda i, this: 'weibo' in pq(this).attr('href'))
			users_info = pq(each)('dd.details')('p').eq(2)('a').filter(lambda i, this: 'users' in pq(this).attr('href'))
			photos_info = pq(each)('dd.details')('p').eq(2)('a').filter(lambda i, this: 'photos' in pq(this).attr('href'))
			if weibo_info:
				weibo = pq(weibo_info).text()
			if users_info:
				users = pq(users_info).text()
			if photos_info:
				photos = pq(photos_info).text()
			page_str += '$'.join([name, addr, weibo, users, photos, str(pos)]) + '*'

		# # 是否有下一页
		# next_p = pq(r)('a').filter(lambda i, this: pq(this).attr('action-type') == 'feed_list_page_next')
		# if next_p and i < 10:
		# 	# print pq(next_p).attr('href')
		# 	num = pq(next_p).attr('href').split('/')[-1]
		# 	# print num
		# 	next_url = 'http://place.weibo.com'+pq(next_p).attr('href')
		# 	# print next_url
		# 	next_url = '/'.join(next_url.split('/')[:-1])
		# 	next_url = re.sub(r'(?<=page=).*?(?=&keyword)', str(num), next_url)
		# 	print next_url
		# 	page_str += parse_page(query_weibo(next_url))
	return page_str

def main():
	# 最后大众点评上700+的mall只能在weibo上query到500+
	existed = {}
	import sys
	fin = sys.argv[1]
	fout = open(sys.argv[2], 'w')
	res_list = load_data(fin)
	for keyword in res_list:
		if keyword in existed:
			continue
		existed.setdefault(keyword, None)
		print keyword
		url = baseurl.format(keyword)
		text = query_weibo(url)
		res = parse_page(text)
		if not res: # 如果没有搜索结果就query下一个，不保存任何结果
			"no result"
			continue
		else:
			fout.write(keyword + '*' + res.encode('utf-8') + '\n')
	fout.close()

if __name__ == '__main__':
	main()
