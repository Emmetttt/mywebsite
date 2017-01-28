import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests

#def RetrieveInfo():
page = "https://www.theguardian.com/world"
    
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
urllibpage = requests.get(page,headers=headers)
soup = BeautifulSoup(urllibpage.text, "lxml")

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

'''    mytrs = soup.findAll("tr")
    #print(mytrs)

    albumNames = []
    albumScores = []
    albumYears = []

    for score in soup.findAll("span", { "class" : "metascore_w small release positive"}):
        albumScores.append(score.string)'''

