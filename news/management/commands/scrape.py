from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from news.models import News
from news.forms import NewsForm

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests

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

	###Loop to delete any duplicate spaces, or \n new line operators
	i = 0
	while i < len(articles):
		articles[i][0] = articles[i][0].replace("\n", "")
		articles[i][0] = articles[i][0].replace("  ", " ")
		if articles[i][0][0] == " ": ##If first character is a space, deletes the first character
			articles[i][0] = articles[i][0][1:]
		if articles[i][0][0] == " ": ##If first character is a space, deletes the first character
			articles[i][0] = articles[i][0][1:]
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

def news(request):
	guardian_world = guardian(topic="international")
	bbc_world = bbc(topic="news/world") 
	telegraph_world = telegraph(topic="news/world")

	guardian_uk = guardian(topic="uk-news")
	bbc_uk = bbc(topic="news/uk") 
	telegraph_uk = telegraph(topic="news/uk")

	guardian_everton = guardian(topic="football/everton")
	bbc_everton = bbc(topic="sport/football/teams/everton")
	telegraph_everton = bbc(topic="everton-fc/")

	guardian_football = guardian(topic="football")
	bbc_football = bbc(topic="sport/football") 
	telegraph_football = telegraph(topic="football")

def save_to_db(info, source, tag):
	for x in info:
		instance = NewsForm().save(commit=False)
		instance.headline = x[0]
		instance.url = x[1]
		instance.source = source
		instance.tag = tag
		instance.save()		

class Command(BaseCommand):
	help = 'Scrapes the news websites'

	def handle(self, *args, **options):
		News.objects.all().delete()

		guardian_world = guardian(topic="international")
		bbc_world = bbc(topic="news/world") 
		telegraph_world = telegraph(topic="news/world")
		save_to_db(guardian_world, 'guardian', 'world')
		save_to_db(bbc_world, 'bbc', 'world')
		save_to_db(telegraph_world, 'telegraph', 'world')

		guardian_uk = guardian(topic="uk-news")
		bbc_uk = bbc(topic="news/uk") 
		telegraph_uk = telegraph(topic="news/uk")
		save_to_db(guardian_uk, 'guardian', 'uk')
		save_to_db(bbc_uk, 'bbc', 'uk')
		save_to_db(telegraph_uk, 'telegraph', 'uk')

		guardian_everton = guardian(topic="football/everton")
		bbc_everton = bbc(topic="sport/football/teams/everton")
		telegraph_everton = bbc(topic="everton-fc/")
		save_to_db(guardian_everton, 'guardian', 'everton')
		save_to_db(bbc_everton, 'bbc', 'everton')
		save_to_db(telegraph_everton, 'telegraph', 'everton')

		guardian_football = guardian(topic="football")
		bbc_football = bbc(topic="sport/football") 
		telegraph_football = telegraph(topic="football")
		save_to_db(guardian_football, 'guardian', 'football')
		save_to_db(bbc_football, 'bbc', 'football')
		save_to_db(telegraph_football, 'telegraph', 'football')
