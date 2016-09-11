## code written by will nowak
# date  = aug / sept 2016
# purpose of this file = scrape content of MR posts.


# to do 
# use bag of words 
# split test and train
# to do tree classification


#import libraries
import re
from bs4 import BeautifulSoup
import requests
import urllib2
import csv
# import functions from my code
from otherfunctions import getLink # from my other file. 
from otherfunctions import makesoup  # from my other file. 
import pandas as pd #pandas for DataFrame organization
from nltk.corpus import stopwords # for stopwords (commonly used words to ignore)
import nltk # for stopwords

# get content for just today. today is "soup"
## make use of makesoup and getLink functions written in marginalrev/otherfunctions.py
## currently, scraping from sept. 4 2016
today= makesoup(getLink(2016,9,4))

# findall div pf content finds posts
## [2] index, for example, shows that this is the third post of the day
postThree=today.find_all('div', {'class' : 'pf-content'})[2]



# this function looks through a given post's soup and finds block quoted material
## function returns a list of block quoted material, with each entry a <p> tag
def findquotes(post): 
	Bqsptags=[] # this is where quoted <p>s go 
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
	return str(words) #return string list of <p> tags

def getposttext(stri):
	beautySoup=BeautifulSoup(stri,"html5lib")
	postText=beautySoup.get_text()
	return postText

# print findauthoredwords(postThree,findquotes(postThree))# this is first paragraph


# test to see if i can successfully scrape posts for multiple days
# loop through all posts of given day


def findNumberofLinks(stri):
	beautySoup=BeautifulSoup(stri,"html5lib")
	numbofLks=len(beautySoup.find_all("a"))
	return numbofLks


years=[2015] #years
months=range(1) # number of months
days = range(3) # number of days
df=pd.DataFrame()


for i in days: # loop through days
	day=makesoup(getLink(2015,1,i+1))
	postcontent=[]
	numberofLinks=[]
	for j in range(len(day.find_all('div', {'class' : 'pf-content'}))):
		post=day.find_all('div', {'class' : 'pf-content'})[j]
		quotes=findquotes(post) #find quotes for post j on day i
		postcontent.append({ # make list with these elements
			'author':BeautifulSoup(str(day.find_all('span',class_='meta_author_name')[j]),"html5lib").a.contents,
			# above code looks at a post and finds author
			'text':getposttext(findauthoredwords(post,quotes)),
			'number of links':findNumberofLinks(findauthoredwords(post,quotes)), #find links in non-quoted material. perhaps another useful feature?
			'date':str(years)+'month ='+ str(1)+ 'day='+str(i), # rough way to identify date
			'post number': j}) #id the post number
		oneDay=pd.DataFrame(postcontent) # make a pd dataframe out of this list
	df = pd.concat([df,oneDay],ignore_index=True) #concat data frames, ignore index so that we have non-repeating indices



print df.shape
print df.columns.values

# print df['text'][0]  #this is a string object

# df.to_csv('out.csv') # export for kicks
# nltk.download()

# print 'a' in stopwords.words("english") 

# rely on kaggle heavily here
# https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words


def review_to_words( raw_review ):
    # Function to convert a text to a processed string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #

    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", raw_review) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))  





# print review_to_words(df['text'][0]) #this works to do what we wanted. clean text for first post shown here

num_text= df["text"].size # number of rows
clean_train_text = []

for i in xrange( 0, num_text ):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    clean_train_text.append( review_to_words( df["text"][i] ) )
    if( (i+1)%3 == 0 ):
    	print "text %d of %d\n" % ( i+1, num_text )                                                                    

# print clean_train_text

# DO SKLEARN

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(analyzer = "word",   
                             tokenizer = None,    
                             preprocessor = None, 
                             stop_words = None,   
                             max_features = 500) 

train_data_features = vectorizer.fit_transform(clean_train_text)

train_data_features = train_data_features.toarray()

print train_data_features.shape

vocab = vectorizer.get_feature_names()
print vocab

from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators = 10)

print df['author'][0][0]





