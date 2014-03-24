#!/usr/bin/python27

from bs4 import BeautifulSoup
import requests
import re


#The ultimate source of all of the song titles
site = "http://en.wikipedia.org/"

#First we get the main page
r = requests.get(site + "wiki/List_of_Billboard_number-one_singles")
data = r.text
soup = BeautifulSoup(data)


#Next we will grab all the hyperlinks that go to the yearly lists of top songs
#One feature that complicates this task slightly is that there are two sets of
#links that we want on the page - the "Pre-Hot 100 Era" and the "Hot 100 Era".
#However, they are each in a different type of html element. Additionally, the
#pages in both of the sections list the songs in a different format. Because 
#of this, we will handle each section separately and bring the results together


#We will begin with the links from the Pre-Hot 100 Era

#We know from looking at the html of the source page that all of the links we 
#want have a similarly-formed title attribute, so we start by grabbing all of 
#the elements on the page that have that kind of title (these will only be
#links)

preHot100Links =  soup.find_all(attrs={'title':re.compile(r".*\bList of Billboard number-one singles of [0-9]{4}\b$")}):

#It turns out that there are two copies of each link on the page. We only want
#one copy of each link so we will put all of these links into a set which will
#deduplicate these for us.

preHot100Set = set(preHot100Links)

#Now we will go through each link in the set, go to its referenced page, and
#extract the top song for each week
for link in preHot100Set:

  #Grab the actual url of the link from each element
  url = link.get('href')

  #print(url)
  #There is just one link that we don't want but is caught by our regex
  #We will simply skip it when we see it
  if url == '/wiki/List_of_Billboard_number-one_singles_of_1958#Hot_100':
    continue

  #follow each link
  yearPage = requests.get(site + url)

  #For each week of each year, we will want to record the top song

  #We will record the specific year we are dealing with 
  yearPageYear = url[-4:]

  #assign song variable
  
  #assign artist variable



