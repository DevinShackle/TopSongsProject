#!/usr/bin/python27

import os


#argv should take a directory containing only the lyrics files as .txt

#define corpus maker function that reads in each file from argv and makes a dict with key:value as song|artist:[lyrics]
#each lyrics file should be named MM-DD-YYYY-song-artist.txt
def corpusMaker (path):
  corpus = {}
  documentVectors = {}
    for lyricFile in os.listdir(path):
      songInfo = lyricFile.name.split('.')[0]
      songData = songInfo.split('-')
      corpus[songInfo] = dict([('date',songData[0]+'-'+songData[1]+'-'+songData[2]),('month',songData[0]),('day',songData[1]),('year',songData[2]),('song',songData[3]),('artist',songData[4])])

      corpus[songInfo]['lyricsVector'] = {}

      with open(lyricFile) as rawLyrics:
        lyrics = rawLyrics.read()
        for word in lyrics.split():
          if word in corpus[songInfo]['lyricsVector']:
            corpus[songInfo]['lyricsVector'][word] += 1
          else:
            corpus[songInfo]['lyricsVector'][word] = 1

          if word in documentVectors:
            documentVectors[word] += 1
          else:
            documentVectors[word] = 1


  return [corpus,documentVectors]


#define TF-IDF function
#takes a corpus and documentVectors
#outputs vectors
def tfidf (corpus, documentVectors):

  tfidfWeightedTermVectors = {}

  idfWeightedDocumentVectors = idf(documentVectors)
  
  for song in corpus:
    tfidfWeightedTermVectors[song] = {}
    for word in corpus[song]['lyricsVector']:
      tf = corpus[song]['lyricsVector'][word]
      idf = idfWeightedDocumentVectors[word]
      tfidfWeightedTermVectors[song][word] = tf * idf

  return tfidfWeightedTermVectors


#define IDF function
def idf (corpus,documentVectors):
  idfWeightedDocumentVectors = {}
  totalDocs = len(corpus)
  for word in documentVectors:
    idfWeightedDocumentVectors[word] = 1.0 / (documentVectors[word]/totalDocs)

  return idfWeightedDocumentVectors

#define cosine similarity function
  


#define jaccard similarity function

