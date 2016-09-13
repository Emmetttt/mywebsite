from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests

from .models import Band
from .forms import BandForm

def RetrieveInfo(name):
    artistnamedash = name.replace(" ", "-")
    artistname = artistnamedash.lower()
    page = "http://www.metacritic.com/person/" + artistname

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
    urllibpage = requests.get(page,headers=headers)
    soup = BeautifulSoup(urllibpage.text, "lxml")
    mydivs = soup.findAll("table", { "class" : "credits person_credits" })
    mytrs = soup.findAll("tr")
    #print(mytrs)

    Months = {'Jan': '01',
          'Feb': '02',
          'Mar': '03',
          'Apr': '04',
          'May': '05',
          'Jun': '06',
          'Jul': '07',
          'Aug': '08',
          'Sep': '09',
          'Oct': '10',
          'Nov': '11',
          'Dec': '12'}

    albumNames = []
    albumScores = []
    albumYears = []

    for score in soup.findAll("span", { "class" : "metascore_w small release positive"}):
        albumScores.append(score.string)

    for year in soup.findAll("td", { "class" : "year" }):
        alyear = year.string
        albumYears.append(alyear.strip())

    i = 0

    for date in albumYears:
        for word, initial in Months.items():
            albumYears[i] = albumYears[i].replace(word, initial)
        if albumYears[i][4] == ',':
            albumYears[i] = albumYears[i][:3] + '0' + albumYears[i][3:]
        albumYears[i] = albumYears[i].replace(" ", "")
        albumYears[i] = albumYears[i].replace(",", "")
        albumYears[i] = albumYears[i][-4:] + '.' + albumYears[i][:4]
        albumYears[i] = float(albumYears[i])
        i = i + 1

    j = 0

    for score in albumScores:
        albumScores[j] = int(float(albumScores[j]))
        j = j + 1


    for name in soup.findAll("a", href=re.compile('^/music/')):
        albumNames.append(name.string)

    k = 0
    data = []
    for value in albumScores:
        #data.append([albumScores[k], albumYears[k]])
        data.append([albumYears[k], albumScores[k]])
        k = k + 1

    #all_together = list(zip(albumNames[2:], albumScores, albumYears))
    return albumNames, albumScores, albumYears, data

def band_input(request):
    if request.method == "POST":
        Bform = BandForm(request.POST)
        if Bform.is_valid():
            bandname = Bform.cleaned_data.get('band_input')
            albumname = RetrieveInfo(Bform.cleaned_data.get('band_input'))[0]
            albumscore = RetrieveInfo(Bform.cleaned_data.get('band_input'))[1]
            albumdate = RetrieveInfo(Bform.cleaned_data.get('band_input'))[2]
            data = RetrieveInfo(Bform.cleaned_data.get('band_input'))[3]
            return render(request, 'music_grapher/graph.html', {'bandname': bandname, 'albumname': albumname, 'albumscore': albumscore, 'albumdate': albumdate, 'data': data})
    else:
        Bform = BandForm()
    return render(request, 'music_grapher/index.html', {'Bform': Bform})

 


def graph(request):
    return render(request, 'music_grapher/graph.html', {})
