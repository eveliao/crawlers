# coding:utf-8

from test_re_placename import cnParse

class Position(object):
	"""docstring for Position"""
	name = ''
	road = ''
	weiboNum = 0
	longitude = -1.0;
	latitude = -1.0;
	def __init__(self, name):
		self.name = name

def readWeiboResult(fileName):
	posList = []
	try:
		f = open(fileName, 'r')
	except IOError:
		print "Error: can\'t find file", fileName
	else:
		for line in f:
			line = line.decode('utf-8')
			parts = line.split('*')
			pos = Position(parts[0])
			posList.append(pos) # 存储所有的有信息mall
			roadAndNum = {}
			if len(parts) < 2:
				continue
			# 取第一个搜索结果的coordinate
			pos.longitude, pos.latitude = eval(parts[1].split('$')[-1]) 

			for subpart in parts[1:-1]:
			# subpart = 上海环球金融中心$上海市浦东新区世纪大道100号（观光厅入口在东泰路靠近花园石桥路）$28672$20233$15252$(31.241, 121.514)
				roadName = preprocessAddr(subpart.split('$')[1]) # 解析出道路名
				roadName = cnParse(roadName)['road']
				roadAndNum.setdefault(roadName, 0)
				weibo = subpart.split('$')[2]
				if weibo != '':
					roadAndNum[roadName] += int(weibo) # 给相应的道路名处的微博数更新
			# 将存储road:weibo的dict转成tutple list,便于排序
			l = [(i, roadAndNum[i]) for i in roadAndNum]
			l.sort(lambda a, b: b[1] - a[1]) # l是一个tuple list，每一个tuple对应key-value

			# 拿到微博数最多的roadName和weiboNum
			for i in range(len(l)):
				if l[i][0] != None: # 这样避免key=None的情况
					pos.road = l[i][0]
					pos.weiboNum = l[i][1]
					break
	return posList
	# 有的address中解析不出road这个key，那么l中就会存在key=None
		

def getResultShow(posList):
	import matplotlib.pyplot as plt
	x1 = [pos.longitude for pos in posList[:400]]
	y1 = [pos.latitude for pos in posList[:400]]

	x2 = [pos.longitude for pos in posList[400:800]]
	y2 = [pos.latitude for pos in posList[400:800]]

	x3 = [pos.longitude for pos in posList[800:1200]]
	y3 = [pos.latitude for pos in posList[800:1200]]

	plot1, = plt.plot(x1, y1, 'ro', label = u'前400/2939')
	# plot2, = plt.plot(x2, y2, 'bo', label = u'前800/2939')
	# plot3, = plt.plot(x3, y3, 'go', label = u'前1200/2939')
	
	plt.title('Business Sites in Shanghai')
	plt.xlabel('longitude')
	plt.ylabel('latitude')
	plt.legend([plot1], ['400/7425'])
	plt.show()

def preprocessAddr(s):
	# 上海市浦东新区世纪大道100号（观光厅入口在东泰路靠近花园石桥路）
	# 去除一些空白符、括号等
	import re
	# 去掉括号包裹的内容
	pat = re.compile('[\(\uff08].*?[\)\uff09]')
	if isinstance(s, unicode):
		pass
	elif isinstance(s, str):
		s = s.decode('utf-8')
	else:
		raise ValueError, "the argument must be a string"
	# 处理空白符制表符等
	s = re.sub(re.compile('\\s'), "", s)
	return re.sub(pat, '', s)

if __name__ == '__main__':
	posList = readWeiboResult("result_business.txt")
	posList.sort(lambda a, b: b.weiboNum - a.weiboNum)
	getResultShow(posList)

