#!/usr/bin/python27

import csv
import os

outoutPath = os.getcwd()+'/data/'
inputPath = os.getcwd()+'/data/lyricsByArtist/'

artists = {}

with open('data/uniqueVStotalByArtist.tsv','w+') as output:
  outputWriter = csv.writer(output,delimiter='\t')
  
  #for each file in the lyricsByArtist directory:
  for filename in os.listdir(inputPath):
 
    print("now processing " + filename)   
    artist = filename[:-4]

    #get the actual lyrics
    with open(inputPath+filename, 'rb') as lyricsFile:
      lyrics = lyricsFile.read()
      #split the lyrics into individual words
      words = lyrics.split()
      totalWords = len(words)
      uniqueWords = len(set(words))
      ratio = float(uniqueWords)/float(totalWords)
      outputWriter.writerow([artist,uniqueWords,totalWords,ratio])
