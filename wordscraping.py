#imports
from bs4 import BeautifulSoup
import requests
import urllib2
import csv
from otherfunctions import getLink
from otherfunctions import makesoup 

# add this to the scrape function built elsewhere.

# get content for just today. today is "soup"
today= makesoup(getLink(2016,9,4))

# this is the third post on the day of 'today'
postThree=today.find_all('div', {'class' : 'pf-content'})[2]


print postThree.find_all('p')

def findquotes(post): # this function looks through a given post's soup and finds block quoted material
						# and returns a list with each entry a <p> tag
	Bqsptags=[]
	for i in range(len(post.find_all('blockquote'))):
		x= post.find_all('blockquote')[i]
		for j in range(len(x.find_all('p'))):
			Bqsptags.append(x.find_all('p')[j])
	return Bqsptags


print findquotes(postThree)

def findauthoredwords(post,quotelist): # this function takes a list of quoted <p> tags and a post. it looks through <p> 
										#tags of post and compares to blockquote. 
										#if not equal, it throws these unique words in an array
	words=[] # this is where unique words written by authot wil go 
	quote=0 #which quote do i want to look at 
	# go through every <p> tag
	for i in range(len(post.find_all('p'))): # for through all <p> tags
	# see if p tag matches one from blockquote. if so, pass and iterate quote variable
		try: # use try/except so that posts without quotes work. this code is likely super SLOW
			if post.find_all('p')[i]==quotelist[quote]:
				quote=quote+1
			else: # if they dont match, then this line was written by the author and we want it
				words.append(post.find_all('p')[i])
		except:
			words.append(post.find_all('p')[i])
	return words


print findauthoredwords(postThree,findquotes(postThree))[0]








