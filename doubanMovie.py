# -*- coding: utf-8 -*-
#http://127.0.0.1
import urllib2
import re
import time

#Greatly inspired by douban_movies (jxgx072037 ), Thanks
#-----------------------------------------------------------------------------
#配置参数，按需修改
tag = '恐怖'   #什么标签
endPage = 20   #搜索多少页
scoreFloor = 7.0   #你能接受的评分底线是多少
userID = 49478062  #这里是我自己的id，换成你的，在个人主页那里的浏览器栏上面找长得跟这个像的数字

#-----------------------------------------------------------------------------
#读取我看过的电影到当前目录的movieTxt中，建议运行一次以后就把这部分屏蔽掉，太花时间。
myMovieTxt = open('movieTxt', 'w')
myWatchedMovie = []

#抓取第一页的html内容
myhtmlMovie0=urllib2.urlopen('http://movie.douban.com/people/'+str(userID)+'/collect').read()
myhtmlMovie = re.findall('href="http://movie.douban.com/subject/\S{1,}?"', myhtmlMovie0)
i = 0
for link in myhtmlMovie:
	if i%2 == 0:
		movieID = link[38:-2]
		myWatchedMovie.append(movieID)
		myMovieTxt.write(movieID+'\n')
		i = i+1
	else:
		i = i+1
		continue

start = 15
while start <502:
	print start
	myhtmlMovieIte0 = urllib2.urlopen('http://movie.douban.com/people/'+str(userID)+'/collect?start=' + str(start) + '&sort=time&rating=all&filter=all&mode=grid').read()
	myhtmlMovieIte = re.findall('href="http://movie.douban.com/subject/\S{1,}?"', myhtmlMovieIte0)
	i = 0
	for link in myhtmlMovieIte:
		if i%2 == 0:
			movieID = link[38:-2]
			myWatchedMovie.append(movieID)
			myMovieTxt.write(movieID+ '\n')
			i = i+1
		else:
			i = i+1
			continue
	start = start + 15


print len(myWatchedMovie)
myMovieTxt.close()

#-----------------------------------------------------------------------
#获得之前保存的我看过的电影list

myMovieList = []
with open('movieTxt', 'r') as f:
    myMovieList = f.read().splitlines()


#-----------------------------------------------------------------------
#获取按评价排序的电影list


scoreList = []
titleList = []

#先把所有的id都放在这个set里
movieAll = []

#再重新reorder一次来避免重复
movieReorder = []


htmlFile = urllib2.urlopen('http://movie.douban.com/tag/'+str(tag)+'?type=O').read()
htmlReg=re.findall('href="http://movie.douban.com/subject/\S{1,}?/"',htmlFile)   
scoreReg = re.findall('<span class="rating_nums">\S{1,}?</span>',htmlFile)
titleReg=re.findall('title=".{1,}?"',htmlFile) 


for link in htmlReg:
	movieID = link[38:-2]
	movieAll.append(movieID)

for link in scoreReg:
	ratingAvg = link[26:-7]
	scoreList.append(ratingAvg)

j = 0
while j < len(scoreReg):
	titleList.append(titleReg[j][7:-1])
	j+=1

start = 20
while start < endPage*20:
	print '开始从第'+str(start)+'个开始抓取'
	htmlFile = urllib2.urlopen('http://movie.douban.com/tag/'+str(tag)+'?start='+str(start)+'&type=O').read()
	htmlReg=re.findall('href="http://movie.douban.com/subject/\S{1,}?/"',htmlFile) 
	scoreReg = re.findall('<span class="rating_nums">\S{1,}?</span>',htmlFile)
	titleReg=re.findall('title=".{1,}?"',htmlFile) 


	for link in htmlReg:
		movieID = link[38:-2]
		movieAll.append(movieID)  

	for link in scoreReg:
		ratingAvg = link[26:-7]
		scoreList.append(ratingAvg)

	j = 0
	while j < len(scoreReg):
		titleList.append(titleReg[j][7:-1])
		j+=1

	start = start+20

i = 0
while i < len(movieAll):
	movieReorder.append(movieAll[i])
	i = i+2
# print len(movieReorder)
# print len(scoreList)
# print len(movieReorder)



#写到html文件里面
f=file('Douban_movies.html','w')
f.write('<!DOCTYPE html>\n<html>\n<head>\n')
f.write('<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n')
f.write('</head>\n\n<body>\n')
f.write('<h1>我的豆瓣电影榜单</h1>'+' '+'<h3>初版</h3>')  #标题


numRemain = 0
i = -1
while i < len(movieReorder)-1:
	i += 1
	print i
	movieID = movieReorder[i]
	if movieID not in myMovieList:
		# time.sleep(2)
		score = scoreList[i]
		title = titleList[i]
		# thisMovie =  client.movie.get(int(movieID))
		# score = thisMovie['rating']['average']
		if float(score) > scoreFloor:
			numRemain += 1
			link = 'http://movie.douban.com/subject/'+str(movieID)+'/'	
			# title = thisMovie['title'].encode('utf8')
			f.write('<p>'+str(numRemain)+'. '+'<a href=\"'+link+'\">'+title+'</a>'+'得分：'+str(score)+'分；'+'\n')
			# f.write('<p>'+str(numRemain)+'. '+'<a href=\"'+i[3]+'\">'+thisMovie['title']+'</a>'+'，共'+i[1]+'人评价，'+'得分：'+i[2]+'分；'+'\n')
			# print thisMovie['title'].encode('utf8')

f.write('</body>')
f.close()
print '完成！请查看html文件，获取豆瓣电影榜单。'

		


