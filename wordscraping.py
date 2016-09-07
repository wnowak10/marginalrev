# code written by will nowak
# date  = aug / sept 2016
# purpose of this file = scrape content of MR posts.

# progress so far = find <p> tags that are not a part of block quotes. 
##MR blog commonly uses block quotes. since i am analyzing MR blog, i dont want to 
## parse and analyze text of block quotes (at least not for now)

# to do: 1. determine how to best export post content for ML analysis
## 2. think of other feature engineering would be best done in python?
## 2a. potentially # of links in a post? cowen more often includes posts that are just links
##  3. add this functionality to my otherfunctions module so that i can get much data from one post all 
## exported to a csv

#import libraries
from bs4 import BeautifulSoup
import requests
import urllib2
import csv
# import functions from my code
from otherfunctions import getLink
from otherfunctions import makesoup 


# get content for just today. today is "soup"
## make use of makesoup and getLink functions written in marginalrev/otherfunctions.py
## currently, scraping from sept. 4 2016
today= makesoup(getLink(2016,9,4))

# findall div pf content finds posts
## [2] index, for example, shows that this is the third post of the day
postThree=today.find_all('div', {'class' : 'pf-content'})[2]


# show all <p> tags for this post
# print postThree.find_all('p')


# this function looks through a given post's soup and finds block quoted material
## function returns a list of block quoted material, with each entry a <p> tag
def findquotes(post): 
	Bqsptags=[]
	for i in range(len(post.find_all('blockquote'))): #how many block quotes are there in post?
		x= post.find_all('blockquote')[i] #set aside a given block quote (x)
		for j in range(len(x.find_all('p'))): # find all the <p> tags
			Bqsptags.append(x.find_all('p')[j]) # append them to a list
	return Bqsptags


# print the list of quoted <p> tags
# print findquotes(postThree)


# this function takes a list of quoted <p> tags and a post as inputs. 
## function looks through <p> tags of post and compares to <p> of blockquote. 
##if not equal, it throws these unique words in an array. else it just ignores

def findauthoredwords(post,quotelist): 
	words=[] # this is where unique words written by author will go 
	quote=0 #which quote do i want to look at 
	# go through every <p> tag
	for i in range(len(post.find_all('p'))): # for through all <p> tags of the post
	# see if p tag matches one from blockquote. if so, pass and iterate quote variable
		try: 		# use try/except so that posts without quotes are passed 
					#and <p> tags from these are dropped into words list
			if post.find_all('p')[i]==quotelist[quote]: # is this a quoted <p>?
				quote=quote+1 # if so, move on to the next quote
			else: # if they dont match, then this line was written author and we want in words list
				words.append(post.find_all('p')[i]) #add to words list
		except:
			words.append(post.find_all('p')[i]) # if no blockquote in post, just throw all <p> tags in 
	return words #reutn list of <p> tags


print findauthoredwords(postThree,findquotes(postThree))# this is first paragraph






