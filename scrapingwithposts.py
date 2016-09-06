#imports
from bs4 import BeautifulSoup
import requests
import urllib2
import csv
#import mrscraping  NEED TO FIGURE OUT HOW TO IMPORT FILE!

# add this to the scrape function built elsewhere.

# get content for just today. today is "soup"
today= makesoup(getLink(2016,9,5))



# need to take out block quote. dont want to analyze text that is in block quotes
postThree= today.find_all('div', {'class' : 'pf-content'})[2]


def findquotes(post):
	Bqsptags=[]
	for i in range(len(post.find_all('blockquote'))):
		x= post.find_all('blockquote')[i]
		for j in range(len(x.find_all('p'))):
			Bqsptags.append(x.find_all('p')[j])
	return Bqsptags


# print findquotes(postThree)


def findauthoredwords(post,quotelist):
	words=[] # this is where unique words written by authot wil go 
	quote=0 #which quote do i want to look at 
	# go through every <p> tag
	for i in range(len(post.find_all('p'))): # for through all <p> tags
	# see if p tag matches one from blockquote. if so, pass and iterate quote variable
		if post.find_all('p')[i]==quotelist[quote]:
			quote=quote+1
		else: # if they dont match, then this line was written by the author and we want it
			words.append(post.find_all('p')[i])
	return words


# print findauthoredwords(postThree,findquotes(postThree))








