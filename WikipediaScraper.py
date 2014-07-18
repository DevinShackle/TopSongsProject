#!/usr/bin/python27

from bs4 import BeautifulSoup
import requests
import re
import csv
import io

"""
This project is aimed at comparing the similarity of the top songs from the 
Billboard Hot 100 top charts since 1959 to see if any trends or interesting features can be identified. 
"""

"""
The first portion of this project will involve scraping Wikipedia for the 
name and artist of the top song in each week of each year for which data is
available.
"""

#Our weekly song data will be stored in a dictionary
songs = {}

#The ultimate source of all of the song titles
site = "http://en.wikipedia.org"

#First we get the main page

r = requests.get(site + "/wiki/List_of_number-one_hits_(United_States)")
data = r.text

soup = BeautifulSoup(data)


"""
We know from looking at the html of the source page that all of the links we 
want have a similarly-formed title attribute, so we start by grabbing all of 
the elements on the page that have that kind of title (these will only be
links)
"""

"""
It turns out that there are two copies of each link on the page. We only want
one copy of each link so we will put all of these links into a set which will
deduplicate these for us.
"""


"""
Now we will go through each link in the set, go to its referenced page, and
extract the top song for each week
"""

hot100Links =  soup.find_all(attrs={'title':re.compile(r".*\bList of Billboard Hot 100 number-one singles of [0-9]{4}\b$")})
#print hot100Links
hot100Links = set(hot100Links)

#output for good results
goodOutputFile = io.open('dateSongArtist.csv', 'wb')
goodOutputWriter = csv.writer(goodOutputFile)

#output for bad results
badOutputFile = io.open('badOutput.csv', 'wb')
badOutputWriter = csv.writer(badOutputFile)

for link in hot100Links:

  #Grab the actual url of the link from each element
  url = link.get('href')

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
  songTable = None

  try:
    songTable = yearlyPageSoup.find_all(attrs={'class':'wikitable'})[1]
  except IndexError:
    continue


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

  #grab each row in the table and scrape the data from it
  songTableRows = songTable.find_all('tr')

  prevSong = ""
  prevArtist = ""

  #Now we will go through each row and get the song data from it
  for row in songTableRows:
    #We need to check to see if 
    #print row
    #break 
    
    songInfo = row.find_all("td")

    #skip it if it's empty
    if not songInfo:
      continue

    i = 0
    for dataPoint in songInfo:
      i += 1

    if i == 3:
      #these are the problem children. Need to send these to a file
      #print url 
      badOutputWriter.writerow([url])    

    #we will use this variable to keep track of the song data
    songData = []

    #Next we will grab the week and use it and the year to assemble the date
  
    week = songInfo[0].get_text()
    completeDate = week + ' ' + yearlyPageYear
    songData.append(completeDate.encode('ascii','ignore'))

    #With the date assembled, we need to gather our song data 
    

    if i == 4:      
      #assign song variable
      songTitle = songInfo[1].get_text()
      if songTitle:
        songData.append(songTitle.encode('ascii','ignore'))
        prevSong = songTitle
      else:
        songData.append(prevSong.encode('ascii','ignore'))
      #assign artist variable

      songArtist = songInfo[2].get_text()
      if songArtist:
        songData.append(songArtist.encode('ascii','ignore'))
        prevArtist = songArtist
      else:
        songData.append(prevArtist.encode('ascii','ignore')) 

    if i == 2: 

      songData.append(prevSong.encode('ascii','ignore'))
      songData.append(prevArtist.encode('ascii','ignore'))
    
    #write to output file   
    #print songData
    goodOutputWriter.writerow(songData)

#clean up
goodOutputFile.close()
badOutputFile.close()
