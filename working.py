#library imports
import urllib2
from bs4 import BeautifulSoup
import pandas as pd 
from nltk.corpus import stopwords # for stopwords (commonly used words to ignore)
import nltk # for stopwords
import re
import numpy as np
# from sklearn.cross_validation import train_test_split


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
		try: 
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
			author = post.span.a.contents
			return author
		except:
			pass

	def getComments(self,postnum):
		try:
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
			x =  post.find("a",class_="teaser_comments").span.contents
			return x
		except:
			pass
		# find("p",class_="to_comments")


	def getTime(self,postnum):
		try:
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
			time = post.find("span",class_="meta_time_line").contents
			return time
		except:
			pass

	def getCategories(self,postnum):
		try:
			caters=[]
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
			cats = post.find("span", class_="meta_category_line")
			for i in range(len(cats.find_all("a"))):
				caters.append(cats.find_all("a")[i].contents)
			return caters
		except:
			pass

	def getTitle(self,postnum):
		try:
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
			return post.find("h2").a.contents
		except:
			pass

	def getWordCount(self,postnum):
		try:
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")
			l=post.find("div",class_="pf-content").get_text()
			le=len(l.split())		
			return le
		except:
			pass

	def getWords(self,postnum):
		try:
			post = BeautifulSoup(str(self.posts[postnum]),"html5lib")	
			return post.find("div",class_="pf-content").get_text()
		except:
			pass

# x=day(2014,5,3)
# print x.getWords(0)


# # # boom. prints clean author and post text. it does include quotes. but this is OK for now, methinks
df=pd.DataFrame() # create empty df
postcontent=[] # create list for post content to populate

years=[2010,2011,2012,2013,2014,2015,2016] #years
months=range(12) # number of months

# # need to roll through different number of days per month so i dont reload posts
twentyEightDayMonths=range(28)
thirtyDayMonths=range(30)
thiryOneDayMonths=range(31)

# move try and pass statements inside loops

for i in years:
	for j in months:
		print 'month is '+ str(j+1)
		if j+1 in [1,3,5,7,8,10,12]:
			for k in thiryOneDayMonths: #if in january..., we have 31 days to loop thru
				try:	
					days=day(year=i,month=(j+1),day=(k+1))
					for m in range(days.numberPosts): # how many posts are in the day of interest?
						try:
							# print "day is: "+str(k) +" and month is: " + str(j)+'and post is :'+str(m)
							postcontent.append({ # make list with these elements
							'author':days.getAuthor(m)[0],
							'date':days.getTime(m),
							'categories':days.getCategories(m),
							'title':days.getTitle(m),
							# above code looks at a post and finds author
							'text': days.getWords(m),
							'wordcount':days.getWordCount(m),
							'comment count':days.getComments(m),
							'post number': m}) #id the post number
							oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list
	 					except:
	 						pass
	 			except:
	 				pass
 		elif j+1 in [4,6,9,11]:
			for k in thirtyDayMonths:
				try:
					days=day(year=i,month=(j+1),day=(k+1))
					for m in range(days.numberPosts): # how many posts are in the day of interest?
						try:
							# print "day is: "+str(k) +" and month is: "+ str(j)+'and post is :'+str(m)
							postcontent.append({ # make list with these elements
							'author':days.getAuthor(m)[0],
							'date':days.getTime(m),
							'categories':days.getCategories(m),
							'title':days.getTitle(m),
							# above code looks at a post and finds author
							'text': days.getWords(m),
							'wordcount':days.getWordCount(m),
							'comment count':days.getComments(m),
							'post number': m}) #id the post number
							oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list
						except:
							pass	
				except:
					pass		
		elif j+1 in [2]:
			for k in twentyEightDayMonths:
				# print "day is: "+str(k) +" and month is: "+ str(j)
				try:
					days=day(year=i,month=(j+1),day=(k+1))
					for m in range(days.numberPosts): # how many posts are in the day of interest?
						try:
							postcontent.append({ # make list with these elements
							'author':days.getAuthor(m)[0],
							'date':days.getTime(m),
							'categories':days.getCategories(m),
							'title':days.getTitle(m),
							# above code looks at a post and finds author
							'text': days.getWords(m),
							'wordcount':days.getWordCount(m),
							'comment count':days.getComments(m),
							'post number': m}) #id the post number
							oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list
						except:
							pass
				except:
					pass

df = pd.concat([df,oneDay],ignore_index=True) #concat data frames, ignore index so that we have non-repeating indices

print df.shape
print df.columns.values

df.to_csv('posts2.csv', header=True, index=False, encoding='utf-8')

df.to_pickle('posts22.pkl')


