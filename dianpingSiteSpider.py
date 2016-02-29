# coding:utf-8

from crawl_shoppingmall import query_page, parse_page, has_next_page
import requests
import socket
import sys

from pyquery import PyQuery as pq

residence_url = 'http://www.dianping.com/search/category/1/80/g26465'
bussiness_url = 'http://www.dianping.com/search/category/1/80/g26466'

# residence_xuhui_url = 'http://www.dianping.com/search/category/1/80/g26465r2#nav-tab|0|1'

def getUrlByRegion(mainUrl):
	# r 是query_page返回的text
	# 本函数旨在获取大众点评网小区分页下面的按“行政区”划分子url，比如“浦东新区”“黄浦区”等
	regionUrlList = []
	for a in pq(query_page(mainUrl))('#region-nav')('a'):
		regionUrlList.append(pq(a).attr('href')) # url在使用前，前面还要加上http://www.dianping.com
	return regionUrlList

def getSubReg(regUrl):
	# 给一个按region划分的住宅url，为了请求到更多的小区，还需要获取其中按sub region划分的url链接
	subRegUrlList = []
	for a in pq(query_page(regUrl))('#region-nav-sub')('a').filter(lambda i, this: pq(this).text() != u'不限'):
		subRegUrlList.append(pq(a).attr('href'))
	return subRegUrlList

def main():
	url = sys.argv[1]
	fout = sys.argv[2]
	with open(fout, 'w') as f:
		# here we specify the crawl object is bussiness sites.
		for regUrl in getUrlByRegion(url):
			for subUrl in getSubReg('http://www.dianping.com'+regUrl):
				subUrl = 'http://www.dianping.com'+ subUrl.split('#')[0] + 'p'
				i = 1 # 表示第一页
				while True:
					r = subUrl + str(i)
					print r
					text = query_page(r)
					f.write(parse_page(text).encode('utf-8'))
					if has_next_page(text):
						i += 1
					else:
						break

if __name__ == '__main__':
	main()
