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
    name = name.lower() ##lowers all the capitals
    nameDashed = name.replace(' ', '-') ##replace spaces with -
    firstLetter = name.replace('the ', '') ##removes "the " so it can find the first letter of the first name
    page = "http://www.albumoftheyear.org/artists/?id=" + firstLetter[0].upper() ##searches AOTY database for all beggining with first letter

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
    urllibpage = requests.get(page,headers=headers)
    soup = BeautifulSoup(urllibpage.text, "html.parser")
    Link = soup.find('a', href=re.compile('^/artist/[0-9]{1,7}-' + nameDashed)) ##Finds any link in the soup with can link to the beatles page
    Name = re.search('\/artist\/[0-9]{1,7}-(.*?)\/', str(Link)).group(0) ##extracts the links from <a> using regex group(0) prints the first match


    artistPage = 'http://www.albumoftheyear.org/' + Name ##load artist page directly
    urllibpageA = requests.get(artistPage, headers=headers)
    soupA = BeautifulSoup(urllibpageA.text, "html.parser")

    albumYears = []
    albumNames = []
    albumScores = []
    data = []

    for dates in soupA.findAll('div', {"class" : "date"}):
        albumYears.append(int(dates.text)) ##Change to integer from string so it can be graphed properly
        
    for titles in soupA.findAll('div', {"class" : "albumTitle"}):
        name = titles.text
        name = name.replace("'", "")
        albumNames.append(name)

    i=0

    for checkDate in soupA.findAll('div', {"class" : "ratingRowContainer"}):
        if checkDate.contents == []:
            del albumYears[i]
            del albumNames[i]
            ##No i+1 since the length of the list has reduced by 1
        else:
            i = i+1
            
    for scores in soupA.findAll('div', {"class" : "rating"}):
        albumScores.append(int(scores.text))
        
    for j in albumYears:
        if j < 1900:
            del albumYears[j-1]
            del albumNames[j-1]
            del albumScores[j-1]

    k=0

    for value in albumScores: ##Gets data into javascript readable format
        data.append('{name: "' + albumNames[k] + '",x: "' + str(albumYears[k]) + '",y: ' + str(albumScores[k]) + '}')
        data[k] = data[k].replace("'", "")
        k = k+1

    data = str(data).replace("'", "")



    max_date = max(albumYears) + 2
    min_date = min(albumYears) - 2 



    return albumNames, albumScores, albumYears, data, max_date, min_date


def band_input(request):
    if request.method == "POST":
        Bform = BandForm(request.POST)
        if Bform.is_valid():
            bandname = Bform.cleaned_data.get('band_input')
            info = RetrieveInfo(Bform.cleaned_data.get('band_input'))
            albumname = info[0]
            albumscore = info[1]
            albumdate = info[2]
            data = info[3]
            max_date = info[4]
            min_date = info[5]
            bandname = bandname.title()
            Bandform = BandForm()
            return render(request, 'music_grapher/graph.html', {'Bform': Bform, 'bandname': bandname, 'albumname': albumname, 'albumscore': albumscore, 'albumdate': albumdate, 'data': data, 'max_date': max_date, 'min_date': min_date})
    else:
        Bform = BandForm()
    return render(request, 'music_grapher/index.html', {'Bform': Bform})




def graph(request):
    return render(request, 'music_grapher/graph.html', {})
