

#imports
from bs4 import BeautifulSoup
import requests
import urllib2
import csv


# key functions
def getLink(i,j,k):
	baselink="http://marginalrevolution.com/marginalrevolution/"
	return baselink+str(i)+"/"+str(j)+"/"+str(k)# year / month / day

def makesoup(link):
	site=link
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(site,headers=hdr)
	try:
		page = urllib2.urlopen(req)
		soup = BeautifulSoup(page,"html5lib")
		return soup
	except: #need this so when we hit page20 for a given month that doesnt exist, for instance, we can keep going
		pass

def scrape(sou):
	###########################################
	##########################################
	######### get data#####
	######### finish cleaning in R

	soup=sou
	try:
		# AUTHOR NAME
		authorName=soup.find_all("span",class_="meta_author_name")
		nam=[]
		for i in range(len(authorName)):
			post=authorName[i]
			nam.append(post.a.contents)

		# TIME OF POST
		time=soup.find_all("span", class_="meta_time_line")
		times=[]
		for i in range(len(time)):
		  post=time[i]
		  times.append(post.contents)	

			##CATEGORIES
		categs=[]
		categories=soup.find_all("span", class_="meta_category_line")
		for i in range(len(categories)):
			post=categories[i]
			cats=post.find_all("a")
			postcategs=[]
			for j in range(len(cats)):
		 		postcategs.append(cats[j].contents)
		 	categs.append(postcategs)

		# TITLES
		title=[]
		titles=soup.find_all('h2')
		for i in range(len(titles)):
			post=titles[i]
			title.append(post.a.contents)

		## # OF COMMENTS
		##########################
		comments=soup.find_all("span",class_="comments")
		numComments=[]
		for i in range(len(comments)):
		  post=comments[i]
		  numComments.append(post.span.contents)

		# POST CONTENT 
		#########################
		content=soup.find_all('div', {'class' : 'pf-content'})
		# WORD COUNT
		#########################
		numberofWords=[]
		numberofentries=len(content)
		for i in range(numberofentries):
		  post=content[i]
		  le=len(str.split(str(post)))
		  numberofWords.append(le)

		features=zip(nam,title,times,numComments,numberofWords,categs) # put all together

		return features
	except AttributeError: 
		pass

def writenewrowstocsv(features):
	try:
		with open("/Users/wnowak/Desktop/testing.csv", 'a') as f: #use a for append. important in this case!
		  writer = csv.writer(f, delimiter=',')
		  writer.writerows(features)
	except:
		pass
