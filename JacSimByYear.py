#!/usr/bin/python27

import csv
import itertools
import os

#we want to find the average imilartiy score among all songs within a given year so that we can see if lyrical similarity is increasing over time.

#paste in JacSim function
def jacSim(set1,set2):
  num = float(len(set1 & set2))
  denom = float(len(set1 | set2))
  return num / denom

yearSongs = {}
decadeSongs = {}
yearAvgSims = {}
decadeAvgSims = {}

#parse through the file with M|YYYY|Song-Artist
with open('data/Month|Year|Song-Artist.txt','rb') as songList:
  for row in songList:
    row = row.rstrip()
    songInfo = row.split('|')
    year = int(songInfo[1])
    songArtist = songInfo[2]
    decade = int(songInfo[1][:-1])
    if year not in yearSongs.keys():
      yearSongs[year] = {}
    if decade not in decadeSongs.keys():
      decadeSongs[decade] = {}
    #yearSongs[year][songArtist] = {}
    #decadeSongs[decade][songArtist] = {} 
    print('getting song file: ' + songArtist)
    with open('data/cleanedLyrics/' + songArtist + '.txt','rb') as lyricsFile:
      lyrics = lyricsFile.read()
      words = lyrics.split()
      wordSet = set(words)
      yearSongs[year][songArtist] = wordSet
      decadeSongs[decade][songArtist] = wordSet

with open('data/JacSimByYear.txt','w+') as output:
  yearWriter = csv.writer(output,delimiter='\t')
  yearWriter.writerow(['year','Song1','Song2','Jaccard Similarity'])
  #get the similarity of each years and decades worth of songs 
  for year in yearSongs.keys():
    pairs = itertools.combinations(yearSongs[year].keys(),2)
    simList = []
    for pair in pairs:
      songArtist1 = pair[0]
      songArtist2 = pair[1]
      sim = jacSim(yearSongs[year][songArtist1],yearSongs[year][songArtist2])
      yearWriter.writerow([year,songArtist1,songArtist2,sim])

with open('data/JacSimByDecade.txt','w+') as output:
  decadeWriter = csv.writer(output,delimiter='\t')
  decadeWriter.writerow(['decade','Song1','Song2','Jaccard Similarity'])
  for decade in decadeSongs.keys():
    pairs = itertools.combinations(decadeSongs[decade].keys(),2)
    simList = []
    for pair in pairs:
      songArtist1 = pair[0]
      songArtist2 = pair[1]
      sim = jacSim(decadeSongs[decade][songArtist1],decadeSongs[decade][songArtist2])
      decadeWriter.writerow([decade*10,songArtist1,songArtist2,sim])

