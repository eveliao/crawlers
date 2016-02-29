# crawlers
Some crawlers used in various projects

## 1 大众点评综合商场/小区/商务楼等site的完整抓取

### 示例
抓取如下图页面中每一个item的全部信息，存储到给定的outputfile中
![](http://ww4.sinaimg.cn/large/901f9a6fjw1f1ga2nx9utj20l70jtwgt.jpg)

### 使用方法

> python dianpingSiteSpider.py [url] [outputfile]

例如：
综合商场的url = "http://www.dianping.com/search/category/1/20/g119"
商务楼的url = "http://www.dianping.com/search/category/1/80/g26466"

## 2 place.weibo.com的搜索信息爬取

### 示例
在place.weibo中搜索一个地名，会出现很多搜索结果，每条结果显示了该地点有多少用户check过。
例如，搜索`iapm`，返回的结果如下


![](http://ww2.sinaimg.cn/large/901f9a6fjw1f1gaad8tu1j20ha0kzjul.jpg)


该爬虫即爬取全部的搜索结果，并存储到指定文件

### 使用方法
 1. 打开浏览器，登陆[http://place.weibo.com/](http://place.weibo.com/)，在“审查元素”中找到cookie，如下图：
![](http://ww1.sinaimg.cn/large/901f9a6fjw1f1gagho3z0j20i404975f.jpg)
复制当前cookie的全部内容，替换query_weibodata.py中的`COOKIE`常量，保存即可
 2. 在terminal中运行
 > python query_weibodata.py [inputfile] [outputfile]


 > eg. python crawlers/query\_weiboplace.py mall\_list.txt result\_bigmall.txt
 > 则每次从mall\_list.txt中读取每一行keyword，然后请求place.weibo，最后将结果写入result\_bigmall.txt文件中


### 说明
 1. inputfile的每一行包含了一条需要请求的地名关键字，如"iapm"
 2. 将结果输出到文件时，代码中所用到的分隔符可能会出现在地点的名称/地址等处，如果遇到解析出错的情况，需手动调整
 

## 3 Unwrap place.weibo得到的数据，并进行绘图

### 功能
可以根据site的微博数对所有sites进行排序，提取Top 1000的sites的经纬度坐标并绘图
