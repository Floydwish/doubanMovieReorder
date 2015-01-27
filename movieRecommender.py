# -*- coding: utf-8 -*-
#http://127.0.0.1
#基于简单的原则：看的人数多且评分较高的一般是好电影
import urllib2
import re
import os
import time
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import webbrowser

tag = '科幻'
endPage = 10   #搜索多少页
scoreFloor = 6.9 #你能接受的评分底线是多少
userID = 49478062  #这里是我自己的id，换成你的，在个人主页那里的浏览器栏上面找长得跟这个像的数字

#-----------------------------------------------------------------------------
#读取我看过的电影到当前目录的movieTxt中，建议运行一次以后就把这部分屏蔽掉，太花时间。
# myMovieTxt = open('movieTxt', 'w')
# myWatchedMovie = []

# def appendMoviesElite(htmlFile):
# 	count = 0
# 	soup = BeautifulSoup(htmlFile)
# 	for link in soup.find_all("a", "nbg"):
# 		count += 1
# 		url = str(link.get('href'))
# 		movieID = url[32:-1]
# 		myWatchedMovie.append(movieID)
# 	return count

# myhtmlMovie0=urllib2.urlopen('http://movie.douban.com/people/'+str(userID)+'/collect')
# appendMoviesElite(myhtmlMovie0)

# curIndex = 15
# while True:
# 	print "从第 "+str(curIndex)+"开始抓取"
# 	myhtmlMovie = urllib2.urlopen('http://movie.douban.com/people/'+str(userID)+'/collect?start=' + str(curIndex) + '&sort=time&rating=all&filter=all&mode=grid')
# 	if appendMoviesElite(myhtmlMovie) < 15:
# 		break
# 	else:
# 		curIndex += 15

# longMovieString = ""
# for i in xrange(0,len(myWatchedMovie)):
# 	longMovieString += myWatchedMovie[i]
# 	longMovieString += "\n"

# myMovieTxt.write(longMovieString)
# myMovieTxt.close()

#-----------------------------------------------------------------------
#获得之前保存的我看过的电影list

myMovieList = []
with open('movieTxt', 'r') as f:
    myMovieList = f.read().splitlines()


#-----------------------------------------------------------------------
#获取按评价排序的电影list

MultiDimensionalList = []
urlList = []
titleList = []
ratingList = []
rateNumList = []
coverList = []

def appendMovies(htmlFile):
	count = 0
	soup = BeautifulSoup(htmlFile)
	for link in soup.find_all("a", "nbg"):
		count += 1
		urlList.append(str(link.get('href')))
		#Get movie title
		titleUtf = link.get('title').encode("utf-8")
		title = str(titleUtf[:])
		titleList.append(title)
	for link in soup.find_all("span", "rating_nums"):
	    ratingList.append(float(link.get_text()))
	for link in soup.find_all("span", "pl"):
	    numUtf = link.get_text().encode("utf-8")
	    num = int(numUtf[1:-10])
	    rateNumList.append(num)
	for link in soup.find_all("img"):
		coverList.append( link.get('src'))
	return count

htmlFile = urllib2.urlopen('http://movie.douban.com/tag/'+str(tag)+'?type=O')
appendMovies(htmlFile)
currentIndex = 20
while currentIndex < endPage*20:
	print '开始从第'+str(currentIndex)+'个开始抓取'
	htmlFile = urllib2.urlopen('http://movie.douban.com/tag/'+str(tag)+'?start='+str(currentIndex)+'&type=O')
	if ~ (appendMovies(htmlFile) < 20):
		currentIndex += 20
	else:
		break

numMovies = len(ratingList)
for i in xrange(0,numMovies):
	newMovie = []
	newMovie.append(urlList[i])
	newMovie.append(titleList[i])
	newMovie.append(ratingList[i])
	newMovie.append(rateNumList[i])
	newMovie.append(coverList[i])
	MultiDimensionalList.append(newMovie)

sortedMovieList = sorted(MultiDimensionalList,key=lambda x: x[3], reverse = True)

fileName = 'recommendMovie.html'
f=file(fileName,'w')
f.write('<!DOCTYPE html>\n<html>\n<head>\n')
f.write('<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n')
f.write('</head>\n\n<body>\n')
f.write('<h1>我的豆瓣电影榜单</h1>'+' '+'<h3>第二版</h3>')  #标题

count = 0
for i in xrange(0,numMovies):
	link = sortedMovieList[i][0]
	title = sortedMovieList[i][1]
	rating = sortedMovieList[i][2]
	rateNum = sortedMovieList[i][3]
	cover = sortedMovieList[i][4]
	movieID = link[32:-1]
	if rating >= scoreFloor:
		if movieID not in myMovieList:
			f.write('<p>'+str(count)+'. '+'<img src="'+cover+'">'
				+'<a href=\"'+link+'\">'+title+'</a>'+'得分：'+str(rating)+'分；'
				+'评价人数：'+str(rateNum)+'\n')
			count += 1

f.write('</body>')
f.close()

webbrowser.open('file://' + os.path.realpath(fileName))

		


