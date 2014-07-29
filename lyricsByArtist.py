#!/usr/bin/python27

import csv
import os


inputPath = os.getcwd()+'/data/cleanedLyrics/'
outputPath = os.getcwd()+'/data/lyricsByArtist/'

artists = {}

#input
for filename in os.listdir(inputPath):
  with open(inputPath+filename,'rb') as lyricsFile:

    lyrics = lyricsFile.read()
    #remove any \t from lyrics
    if '\t' in lyrics:
      lyrics = lyrics.replace('\t','')

    #get the artist name
    artistName = filename[filename.find('-')+1:-4]

    #remove featured artists
    if 'featuring' in artistName:
      artistName = artistName[:artistName.find('featuring')]
    if 'Featuring' in artistName:
      artistName = artistName[:artistName.find('Featuring')]

    #remove trailing underscore if needed
    if '_' in artistName[-1]:
      artistName = artistName[:-1]

    #check to see if artist is in artists:
    if artistName in artists:
      artists[artistName] = artists[artistName]+lyrics
    else:
      artists[artistName] = lyrics

#output
for artist in artists.keys():
  #artistName = artist.replace("'",'')
  with open(outputPath+artist+'.txt','w+') as output:
    output.write(artists[artist])

