#!/usr/bin/python27

from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import httplib

host = 'api.chartlyrics.com'

queryPrefix = '/apiv1.asmx/SearchLyricDirect?'

#setting up api connection
conn = httplib.HTTPConnection(host)

lyricsQueried = set()

with open('alreadyHaveLyrics.txt','rb') as alreadyHaveLyrics:
  print('looks like we already have lyrics for these songs:')
  for line in alreadyHaveLyrics:
    print line
    lyricsQueried.add(line.rstrip())

print('we have lyrics for ' + str(len(lyricsQueried)) + ' songs')

with open('alreadyHaveLyrics.txt','a') as alreadyHaveLyrics:
  
  #prep noLyrics file
  with open('noLyrics.csv','a') as noLyrics:
    noLyricsWriter = csv.writer(noLyrics)

    with open('dateSongArtist.csv','rb') as songFile:
      songReader = csv.reader(songFile)
      for song in songReader:
	#setting up api connection
	#conn = httplib.HTTPConnection(host)
	
	print song
	# get song artist and title
	date = song[0]
	title = song[1]
	artist = song[2]

	#check if we've already retrieved the lyrics for this song
	if title+artist in lyricsQueried:
	  print("we already have these lyrics. skipping")
	  continue

	# assemble url query
	queryParams = "song="+title.replace(" ","+")+"&artist="+artist.replace(" ","+")
	queryURL = queryPrefix + queryParams
	conn.request("GET", queryURL)
	response = conn.getresponse()
	lyrics = response.read()

	lyricsQueried.add(title+artist)
	alreadyHaveLyrics.write(title+artist+'\n')
	# check if response contains lyrics
	if 'xml' not in lyrics or '<Lyric>' not in lyrics:
	  #we know that lyrics weren't returned 
	  print("no lyrics found for "+title+" " +artist)
	  noLyricsWriter.writerow(song)
         
	  time.sleep(20)
	  continue

	# parse the xml 
	lyricsStartIndex = lyrics.index('<Lyric>')+7
	lyricsEndIndex = lyrics.index('</Lyric>')
	lyricsTrimmed = lyrics[lyricsStartIndex:lyricsEndIndex]
   
	# clean the lyrics
	lyricsCleaned = lyricsTrimmed.replace('\r\n',' ')

	# create output file
	outputFileName = title.replace(' ','_')+'-'+artist.replace(' ','_')+'.txt'
	
	# write lyrics to lyrics file
	with open('lyrics/'+outputFileName, 'w+') as output:
	  output.write(lyricsCleaned)

	#conn.close()
	# pause so as to not overload server
	time.sleep(20)
   
     
# shut down api connection
conn.close()


