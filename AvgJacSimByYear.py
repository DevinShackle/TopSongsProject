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

#get the similarity of each years and decades worth of songs 
for year in yearSongs.keys():
  pairs = itertools.combinations(yearSongs[year].keys(),2)
  simList = []
  for pair in pairs:
    songArtist1 = pair[0]
    songArtist2 = pair[1]
    sim = jacSim(yearSongs[year][songArtist1],yearSongs[year][songArtist2])
    simList.append(sim)
  #take the average
  avgSim = float(sum(simList))/len(simList)
  yearAvgSims[year] = avgSim 

for decade in decadeSongs.keys():
  pairs = itertools.combinations(decadeSongs[decade].keys(),2)
  simList = []
  for pair in pairs:
    songArtist1 = pair[0]
    songArtist2 = pair[1]
    sim = jacSim(decadeSongs[decade][songArtist1],decadeSongs[decade][songArtist2])
    simList.append(sim)
  #take the average
  avgSim = float(sum(simList))/len(simList)
  decadeAvgSims[decade] = avgSim 

#now write to output files
with open('data/avgJacSimByYear.txt','w+') as output:
  yearWriter = csv.writer(output,delimiter='\t')
  for year in yearAvgSims.keys():
    yearWriter.writerow([year,yearAvgSims[year]])

with open('data/avgJacSimByDecade.txt','w+') as output:
  decadeWriter = csv.writer(output,delimiter='\t')
  for decade in decadeAvgSims.keys():
    decadeWriter.writerow([decade*10,decadeAvgSims[decade]])


