#!/usr/bin/python27

import csv

#read dateSongArtist.csv file
with open('data/dateSongArtist.tsv','rb') as dsa:
  with open('data/dateSongArtistJoinable.tsv','w+') as output:
    outputWriter = csv.writer(output,delimiter='\t')
    for line in dsa:
      print('processing ' + line)
      lineSplit = line.split('\t')
      date = lineSplit[0].split('/')
      month = date[0]
      year = date[2]
      title = lineSplit[1].replace(' ','_')
      artist = lineSplit[2].replace(' ','_')
      outputLine = lineSplit + [month,year,title+'-'+artist]
      for field in outputLine:
        if '\n' in field:
          field.replace('\n','')
      outputWriter.writerow(outputLine)


#read uniqueVStotalWords.tsv file
with open('data/uniqueVStotalWords.tsv','rb') as utw:
  with open('data/uniqueVStotalWordsJoinable.tsv','w+') as output:
    outputWriter = csv.writer(output, delimiter='\t')
    with open('data/uniqueVStotesErrorFile.tsv','w+') as errorFile:
      errorWriter = csv.writer(errorFile, delimiter='\t')
      for line in utw:
        try:
          print('processing ' + line) 
          lineSplit = line.split('\t')
          joinable = lineSplit[1] + '-' + lineSplit[0]
          outputLine = lineSplit + [joinable]
          for field in outputLine:
            if '\n' in field:
              field.replace('\n','')
          outputWriter.writerow(outputLine)
        except:
          print('error on line: ' + line)
          errorWriter.writerow(line)

