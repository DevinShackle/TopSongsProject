#!/usr/bin/python27

import csv
import os

with open('data/uniqueVStotalWords.tsv','w+') as output:
  outputWriter = csv.writer(output,delimiter='\t')
  
  path = os.getcwd()+'/data/cleanedLyrics/'
  #for each file in the cleanedLyrics directory:
  for filename in os.listdir(path):
 
    print("now processing " + filename)   
    #split the filename and clean up the song and artist names
    #find the first '-'
    splitIndex = filename.index('-')

    #the song is what comes before
    song = filename[:splitIndex]

    #the artist is what comes after until '.txt'
    artist = filename[splitIndex+1:-4]

    #get the actual lyrics
    with open(path+filename, 'rb') as lyricsFile:
      lyrics = lyricsFile.read()
      #split the lyrics into individual words
      words = lyrics.split()
      totalWords = len(words)
      uniqueWords = len(set(words))
      ratio = float(uniqueWords)/float(totalWords)
      outputWriter.writerow([artist,song,uniqueWords,totalWords,ratio])
