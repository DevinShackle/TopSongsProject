#!/usr/bin/python27

from bs4 import BeautifulSoup
import requests
import re

r = requests.get("http://en.wikipedia.org/wiki/List_of_Billboard_number-one_singles")

data = r.text

soup = BeautifulSoup(data)
site = "http://en.wikipedia.org/"

#for link in soup.find_all('a'):
#  print(link.get('href'))

for link in soup.find_all(attrs={'title':re.compile(r".*\bList of Billboard number-one singles of [0-9]{4}\b.*")}):

  url = link.get('href')
  #print(link.get('href'))
  if url == '/wiki/List_of_Billboard_number-one_singles_of_1958#Hot_100':
    continue

  #follow each link
  yearPage = requests.get(site + url)

  #assign year variable
  yearPageYear = url[-4:]

  #assign song variable
  
  #assign artist variable



