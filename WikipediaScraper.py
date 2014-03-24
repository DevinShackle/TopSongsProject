#!/usr/bin/python27

from bs4 import BeautifulSoup
import requests
import re

"""
This project is aimed at comparing the similarity of the top songs from the 
Billboard top charts since 1940 to see if any trends or interesting features
can be identified. 
"""

"""
The first portion of this project will involve scraping Wikipedia for the 
name and artist of the top song in each week of each year for which data is
available.
"""

#Our weekly song data will be stored in a dictionary
songs = {}

#The ultimate source of all of the song titles
site = "http://en.wikipedia.org/"

#First we get the main page
r = requests.get(site + "wiki/List_of_Billboard_number-one_singles")
data = r.text
soup = BeautifulSoup(data)

"""
Next we will grab all the hyperlinks that go to the yearly lists of top songs
One feature that complicates this task slightly is that there are two sets of
links that we want on the page - the "Pre-Hot 100 Era" and the "Hot 100 Era".
However, they are each in a different type of html element. Additionally, the
pages in both of the sections list the songs in a different format. Because of 
this, we will handle each section separately and bring the results together


We will begin with the links from the Pre-Hot 100 Era

We know from looking at the html of the source page that all of the links we 
want have a similarly-formed title attribute, so we start by grabbing all of 
the elements on the page that have that kind of title (these will only be
links)
"""

preHot100Links =  soup.find_all(attrs={'title':re.compile(r".*\bList of Billboard number-one singles of [0-9]{4}\b$")}):

"""
It turns out that there are two copies of each link on the page. We only want
one copy of each link so we will put all of these links into a set which will
deduplicate these for us.
"""

preHot100Set = set(preHot100Links)

"""
Now we will go through each link in the set, go to its referenced page, and
extract the top song for each week
"""
for link in preHot100Set:

  #Grab the actual url of the link from each element
  url = link.get('href')

  #print(url)
  #There is just one link that we don't want but is caught by our regex
  #We will simply skip it when we see it
  if url == '/wiki/List_of_Billboard_number-one_singles_of_1958#Hot_100':
    continue

  #follow each link
  yearlyPage = requests.get(site + url)

  #Soupify the page html
  yearlyPageData = yearlyPage.text
  yearlyPageSoup = BeautifulSoup(yearlyPageData)

  #For each week of each year, we will want to record the top song

  #We will record the specific year we are dealing with by looking at the
  #last 4 characters of the url
  yearlyPageYear = url[-4:]

  
  #it turns out that the table on each page with the song information can
  #be easily grabbed because it is the first element with a class of
  #'wikitable'
  songTable = yearlyPageSoup.find(attrs={'class':'wikitable'})

  """
  The table is arranged so that if a given week's top song is the same as 
  the previous week's, the table data elements for the song are not 
  included in the row for that week. When the page is rendered in the 
  browser, this causes the cells containing the song name and artist to 
  stretch down across all of the weeks in which that song was on top. 

  What this means for us is that there will be rows that do not contain
  song data. Because of this, we will need to remember the last song we
  saw and if we encounter a row with no song data, we know that we need
  to use the most recent song we've seen. We know that we can spot the 
  that do not contain song data because they will have only two elements
  instead of four
  """

  #we will use this variable to keep track of the song data
  songData = []

  #grab each row in the table and scrape the data from it
  songTableRows = songTable.find_all('tr')

  #Now we will go through each row and get the song data from it
  for row in songTableRows:
    #We need to check to see if 
  
  #Next we will grab the week and use it and the year to assemble the date
  week = ''

  completeDate = week + ' ' + yearlyPageYear

  #With the date assembled, we need to gather our song data 

  #assign song variable
  
  #assign artist variable



