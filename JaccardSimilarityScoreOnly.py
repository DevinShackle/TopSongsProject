#!/usr/bin/python27

import csv
import itertools
import os


#we will run our simple jaccard similarity here
def jacSim(set1,set2):
  num = float(len(set1 & set2))
  denom = float(len(set1 | set2))
  return num / denom


#go through song list and get each lyric file path

with open('jacSimScoreOnlyOut.tsv','w+') as output:

  outputWriter = csv.writer(output,delimiter='\t')

  # dict to keep all the sets of lyrics
  lyricsDict = {}
  #use lyric path to get each lyric text
  path = os.getcwd()+'/data/cleanedLyrics/'
  for filename in os.listdir(path):

    print("now processing " + filename)
    with open(path+filename,'rb') as lyricsFile:
      lyrics = lyricsFile.read()
      words = lyrics.split()

      #make it a set
      wordSet = set(words)

      #add set to dict
      lyricsDict[filename[:-4]] = wordSet

  #use itertools to compute each pair of lyrics
  pairs = itertools.combinations(lyricsDict.keys(),2)
  for pair in pairs:

    songArtist1 = pair[0]
    songArtist2 = pair[1]
    sim = jacSim(lyricsDict[songArtist1],lyricsDict[songArtist2])
    
    #write sim score and song names to output file
    outputWriter.writerow([sim])
  

