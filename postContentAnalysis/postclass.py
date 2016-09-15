#library imports
import urllib2
from bs4 import BeautifulSoup
import pandas as pd 
from nltk.corpus import stopwords # for stopwords (commonly used words to ignore)
import nltk # for stopwords
import re
import numpy as np
from sklearn.cross_validation import train_test_split


class day(object):
	'''this class takes month, day as inputs.
	a link is created, and urllib2 and
	beautifulsoup are used to create soup.
	other functions make calls on the soup'''

	def __init__(self, year, month,day):
		#instance defs
		self.words= [] #for  authored words in post
		self.posts = [] #list to place blog posts from this day
		self.Bqsptags= [] # this is where quoted <p>s from a given post go 
	  	self.year= year
	   	self.month= month
	   	self.day= day

		baselink="http://marginalrevolution.com/marginalrevolution/"
		dayLink= baselink+str(self.year)+"/"+str(self.month)+"/"+str(self.day)# year / month / day
		self.dayLink=dayLink #create link to MR blog

		hdr = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(self.dayLink,headers=hdr)
		page = urllib2.urlopen(req)
		soup = BeautifulSoup(page,"html5lib") 
		self.dailysoup = soup # create soup for given day

		# self.numberPosts is number of posts for that day
		self.numberPosts = len(self.dailysoup.find_all("div", class_='post_box'))

		# self.posts contains list with posts for the day. 
		#add individual posts to it using for loop.
		for i in range(self.numberPosts):
			self.posts.append(self.dailysoup.find_all("div", class_='post_box')[i])

	def getAuthor(self,postnum):	# require postnum for the author you seek	 
		post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
		author = post.span.a.contents
		return author

	# def findquotes(self,postnum): 
	# 	for i in range(len(self.posts[postnum].find_all('blockquote'))): #how many block quotes are there in post?
	# 		x= self.posts[postnum].find_all('blockquote')[i] #set aside a given block quote (x)
	# 		for j in range(len(x.find_all('p'))): # find all the <p> tags
	# 			self.Bqsptags.append(x.find_all('p')[j]) # append them to a list
	# 	return self.Bqsptags # returns a list of 

	# def uniquewords(self,postnum):
	# 	quote=0
	# 	for i in range(len(self.posts[postnum].find_all('p'))): # for through all <p> tags of the post
	# 		try: 		# use try/except so that posts without quotes are passed 
	# 				#and <p> tags from these are dropped into words list
	# 			if self.posts[postnum].find_all('p')[i]==self.Bqsptags[quote]: # is this a quoted <p>?
	# 				quote=quote+1 # if so, move on to the next quote
	# 			else: # if they dont match, then this line was written author and we want in words list
	# 				self.words.append(self.posts[postnum].find_all('p')[i]) #add to words list
	# 		except:
	# 			self.words.append(self.posts[postnum].find_all('p')[i]) # if no blockquote in post, just throw
	# 	return self.words




# # boom. prints clean author and post text. it does include quotes. but this is OK for now, methinks
df=pd.DataFrame()
postcontent=[]

years=[2013,2014,2015] #years
months=range(12) # number of months

# need to roll through different number of days per month so i dont reload posts
twentyEightDayMonths=range(28)
thirtyDayMonths=range(30)
thiryOneDayMonths=range(31)

for i in years:
	for j in months:
		if j+1 in [1,3,5,7,8,10,12]:
			for k in thiryOneDayMonths: #if in january..., we have 31 days to loop thru
				days=day(year=i,month=(j+1),day=(k+1))
				for m in range(days.numberPosts): # how many posts are in the day of interest?
					postcontent.append({ # make list with these elements
					'author':days.getAuthor(m)[0],
					# above code looks at a post and finds author
					'text': days.posts[m].find("div",class_="pf-content").get_text(),
					'post number': m}) #id the post number
					oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list
 		elif j+1 in [4,6,9,11]:
			for k in thirtyDayMonths:
				days=day(year=i,month=(j+1),day=(k+1))
				for m in range(days.numberPosts): # how many posts are in the day of interest?
					postcontent.append({ # make list with these elements
					'author':days.getAuthor(m)[0],
					# above code looks at a post and finds author
					'text': days.posts[m].find("div",class_="pf-content").get_text(),
					'post number': m}) #id the post number
					oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list
		elif j+1 in [2]:
			for k in twentyEightDayMonths:
				days=day(year=i,month=(j+1),day=(k+1))
				for m in range(days.numberPosts): # how many posts are in the day of interest?
					postcontent.append({ # make list with these elements
					'author':days.getAuthor(m)[0],
					# above code looks at a post and finds author
					'text': days.posts[m].find("div",class_="pf-content").get_text(),
					'post number': m}) #id the post number
					oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list

df = pd.concat([df,oneDay],ignore_index=True) #concat data frames, ignore index so that we have non-repeating indices

print df.shape
print df.columns.values
print df
df.to_csv('posts.csv', header=True, index=False, encoding='utf-8')

df.to_pickle('posts.pkl')


