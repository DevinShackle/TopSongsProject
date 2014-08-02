#!/usr/bin/python27

import csv
import os


songData = {}
with open('data/uniqueVStotalWords.tsv','rb') as uvt:
  for line in uvt:
    line = line.split()
    titleArtist = line[1]+'-'+line[0]
    songData[titleArtist] = {}
    songData[titleArtist]['artist'] = line[0]
    songData[titleArtist]['title'] = line[1]
    songData[titleArtist]['uniqueWords'] = line[2]
    songData[titleArtist]['totalWords'] = line[3]
    songData[titleArtist]['uniqueTotalRatio'] = line[4]

    #if line[1] == 'Michael_Bolton':
    #  print(line)

    #print(songData)

with open('data/uniqueTotalByMonth.tsv','w+') as output:
  outputWriter = csv.writer(output,delimiter='\t')
  headerRow = ['month','year','artist','title','uniqueWords','totalWords','uniqueTotalRatio']
  outputWriter.writerow(headerRow)
  with open('data/Month|Year|Song-Artist.txt','rb') as mys:
    songs = mys.read().split()
    songSet = set()
    for entry in songs:
      songSet.add(entry)

    
    for song in songSet:
      print('processing ' + song)
      data = song.split('|')
      outputRow = []
      outputRow.append(data[0])
      outputRow.append(data[1])
      outputRow.append(songData[data[2]]['artist'])
      outputRow.append(songData[data[2]]['title'])
      outputRow.append(songData[data[2]]['uniqueWords'])
      outputRow.append(songData[data[2]]['totalWords'])
      outputRow.append(songData[data[2]]['uniqueTotalRatio'])
      
      outputWriter.writerow(outputRow)

