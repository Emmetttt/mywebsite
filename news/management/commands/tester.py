import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests

##guardian(topic="international")


def sou(p):
	page = p
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
	urllibpage = requests.get(page,headers=headers)
	soup = BeautifulSoup(urllibpage.text, "lxml")
	return soup


def dictionary(item):
	dic = []
	for x in item:
		info = {}
		info['headline'] = x[0]
		info['url'] = x[1]
		dic.append(info)
	return dic


def guardian(topic):
	link = "https://www.theguardian.com/" + topic
	soup = sou(link)
	articles = []
	mydivs = soup.findAll("a", { "data-link-name" : "article" })
	for x in mydivs:
		articles.append([x.text, x['href']])
		
	subhead = soup.findAll("div", { "class" : "fc-item__standfirst" })
	i=0
	for x in subhead:
		articles[i].append(x.text)
		i+=1


	###Loop to delete any duplicate spaces, or \n new line operators
	i = 0
	while i < len(articles):
		articles[i][0] = articles[i][0].replace("\n", "")
		articles[i][0] = articles[i][0].replace("  ", " ")
		if articles[i][0][0] == " ": ##If first character is a space, deletes the first character
			articles[i][0] = articles[i][0][1:]
		if articles[i][0][0] == " ": ##If first character is a space, deletes the first character
			articles[i][0] = articles[i][0][1:]
		if len(articles[i]) == 3:
			articles[i][2] = articles[i][2].replace("\n", "")
			articles[i][2] = articles[i][2].replace("  ", " ")
			if articles[i][2][0] == " ": ##If first character is a space, deletes the first character
				articles[i][2] = articles[i][2][1:]
			if articles[i][2][0] == " ": ##If first character is a space, deletes the first character
				articles[i][2] = articles[i][2][1:]
		i+=1

	###Loop to delete duplicate entries
	j = 0
	while j < len(articles):
		if j > 0:
			x = articles[j][0].replace(" ", "")
			y = articles[j-1][0].replace(" ", "")
			if x == y:
				del articles[j]
			else:
				j+=1
		else:
			j+=1

	###Loop to delete duplicate headlines
	k=0
	while k < len(articles)-1:
		z = k+1 ##Counts to compare the current headline with all headlines
		a = articles[k] ##Current headline
		while z < len(articles): ##Loop over all articles
			b = articles[z]
			if a[1] == b[1]: ##If they both link to the same article
				del articles[z]
			else:
				z+=1
		k+=1

	articles = articles[:5]

	dicgua = dictionary(articles)
	return articles


def bbc(topic):
	link = "http://www.bbc.co.uk/" + topic
	soup = sou(link)
	bbcarticles = []

	mydivs = soup.findAll("a", { "class" : "title-link" })

	for x in mydivs:
		bbcarticles.append([x.text, 'http://www.bbc.co.uk' + x['href']])

	buzz_sum = soup.findAll("p", { "class" : "buzzard__summary" })

	i = 0

	for x in buzz_sum:
		bbcarticles[i].append(x.text)
		print(x.text)
		i+=1

	pig_sum = soup.findAll("p", { "class" : "pigeon-item__summary" })

	for x in pig_sum:
		bbcarticles[i].append(x.text)
		print(x.text)
		i+=1
	
	bbcarticles = bbcarticles[:5]

	i = 0

	while i < len(bbcarticles):
		bbcarticles[i][0] = bbcarticles[i][0].replace("\n", "")
		i+=1

	dicbbc = dictionary(bbcarticles)

	if dicbbc == []:
		mydivs = soup.findAll("h3", { "class" : "lakeside__title faux-block-link__target gel-pica-bold" })

		for x in mydivs:
			bbcarticles.append([x.text, 'http://www.bbc.co.uk' + x.a['href']])
		
		bbcarticles = bbcarticles[:5]

		i = 0

		while i < len(bbcarticles):
			bbcarticles[i][0] = bbcarticles[i][0].replace("\n", "")
			i+=1

		dicbbc = dictionary(bbcarticles)

	return bbcarticles

def telegraph(topic):
	link = "http://www.telegraph.co.uk/" + topic
	soup = sou(link)
	telearticles = []
	mydivs = soup.findAll("h3", { "class" : "list-of-entities__item-body-headline"})

	for x in mydivs:
	    telearticles.append([x.text, 'http://www.telegraph.co.uk' + x.a['href']])

	telearticles = telearticles[:5]

	i = 0

	while i < len(telearticles):
		telearticles[i][0] = telearticles[i][0].replace("\n", "")
		i+=1

	dictele = dictionary(telearticles)
	return telearticles

def nyt(topic):
	link = "https://www.nytimes.com/" + topic
	soup = sou(link)
	nytarticles = []
	mydivs = soup.findAll("div", { "class" : "story" })
	i=0

	for x in mydivs:
		while i < 20:
			for y in x.findAll("h3"):
				nytarticles.append([y.text, x.a['href']])
			for y in x.findAll("p", { "class" : "summary" }):
				nytarticles[i].append(y.text)
			i+=1

	return nytarticles[1]

