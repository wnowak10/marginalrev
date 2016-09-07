testing <- read.csv("~/Desktop/testing.csv", comment.char="#")
library(reshape2)
library(ggplot2)
library(dplyr)
library(mice)
library(randomForest)

head(testing)
##############
##############
# authors
##############
##############
testing$author=gsub( "\\[u\\'", '', testing$author)
testing$author=gsub( "\\'\\]", '', testing$author)
testing$author=as.factor(testing$author)
testing$author[1:10]
str(testing$author)
nrow(testing)
#clean other authors (glen weyl and ramez naam wrote a few posts)
str(testing[testing$author=="E. Glen Weyl",])
str(testing[testing$author=="Ramez Naam",])
#get rid of these other authors
testing=testing[testing$author=='Tyler Cowen' | testing$author=='Alex Tabarrok',]

testing$author <- factor(testing$author)
levels(testing$author)

##############
##############
# title
##############
##############
testing$title=gsub( "\\[u\\'", '', testing$title)
testing$title=gsub( "\\'\\]", '', testing$title)
testing$title[1:10]

##############
##############
# time
##############
##############
# clean
testing$time=gsub("\\[u\\'",'',testing$time)
testing$time=gsub("\\\\",'',testing$time)
testing$time=gsub("nttttton ",'',testing$time)
testing$time=gsub("tttttat",'',testing$time)
testing$time=gsub("tttt",'',testing$time)
testing$time=gsub("\\'\\]",'',testing$time)
# format as date
testing$time=as.Date(testing$time,format='%B %d, %Y %H:%M %p')
testing$time[1:10] # working

##############
##############
# comment count
##############
##############
testing$numberComments=gsub( ".'", '', testing$numberComments)
testing$numberComments=gsub( "\\]", '', testing$numberComments)
testing$numberComments=gsub( "\\[", '', testing$numberComments)
testing$numberComments=as.numeric(testing$numberComments)
testing$numberComments[1:10]# working, but there are NAs

##############
##############
# word count
##############
##############
testing$numberofWords=as.numeric(testing$numberofWords)
mean(testing$numberofWords,na.rm=T)  # working
sum(is.na(testing$numberofWords)) # 3 na

##############
##############
# categories
##############
##############
# split categories
testing = transform(testing, cats = colsplit(testing$categories,pattern=",",names=seq(10)))
# clean. this works for cat 1. how to loop for all 10 columns?
# create a new column for all of the categories
testing$cats.1=gsub("^[^_]*u\\'", '',testing$cats.1)
testing$cats.1=gsub("\\'.*", '',testing$cats.1)
testing$cats.2=gsub("^[^_]*u\\'", '',testing$cats.2) # gets rid of all before u quote
testing$cats.2=gsub("\\'.*", '',testing$cats.2)
testing$cats.3=gsub("^[^_]*u\\'", '',testing$cats.3)
testing$cats.3=gsub("\\'.*", '',testing$cats.3)
testing$cats.4=gsub("^[^_]*u\\'", '',testing$cats.4)
testing$cats.4=gsub("\\'.*", '',testing$cats.4)
testing$cats.5=gsub("^[^_]*u\\'", '',testing$cats.5)
testing$cats.5=gsub("\\'.*", '',testing$cats.5)
testing$cats.6=gsub("^[^_]*u\\'", '',testing$cats.6)
testing$cats.6=gsub("\\'.*", '',testing$cats.6)
testing$cats.7=gsub("^[^_]*u\\'", '',testing$cats.7)
testing$cats.7=gsub("\\'.*", '',testing$cats.7)
# create dummies. use uncategorized as base case
testing$CurrentAffairs=as.numeric(testing$cats.1=="Current Affairs"|testing$cats.2=="Current Affairs"|testing$cats.3=="Current Affairs"|testing$cats.4=="Current Affairs"|testing$cats.5=="Current Affairs"|  testing$cats.6=="Current Affairs")
testing$Education=as.numeric(testing$cats.1=="Education"|testing$cats.2=="Education"|testing$cats.3=="Education"|testing$cats.4=="Education"|testing$cats.5=="Education"|  testing$cats.6=="Education")
testing$Music=as.numeric(testing$cats.1=="Music"|testing$cats.2=="Music"|testing$cats.3=="Music"|testing$cats.4=="Music"|testing$cats.5=="Music"|  testing$cats.6=="Music")
testing$Philosophy=as.numeric(testing$cats.1=="Philosophy"|testing$cats.2=="Philosophy"|testing$cats.3=="Philosophy"|testing$cats.4=="Philosophy"|testing$cats.5=="Philosophy"|  testing$cats.6=="Philosophy")
testing$PoliticalScience=as.numeric(testing$cats.1=="Political Science"|testing$cats.2=="Political Science"|testing$cats.3=="Political Science"|testing$cats.4=="Political Science"|testing$cats.5=="Political Science"|  testing$cats.6=="Political Science")
testing$Science=as.numeric(testing$cats.1=="Science"|testing$cats.2=="Science"|testing$cats.3=="Science"|testing$cats.4=="Science"|testing$cats.5=="Science"|  testing$cats.6=="Science")
testing$History=as.numeric(testing$cats.1=="History"|testing$cats.2=="History"|testing$cats.3=="History"|testing$cats.4=="History"|testing$cats.5=="History"|  testing$cats.6=="History")
testing$Law=as.numeric(testing$cats.1=="Law"|testing$cats.2=="Law"|testing$cats.3=="Law"|testing$cats.4=="Law"|testing$cats.5=="Law"|  testing$cats.6=="Law")
testing$Games=as.numeric(testing$cats.1=="Games"|testing$cats.2=="Games"|testing$cats.3=="Games"|testing$cats.4=="Games"|testing$cats.5=="Games"|  testing$cats.6=="Games")
testing$Books=as.numeric(testing$cats.1=="Books"|testing$cats.2=="Books"|testing$cats.3=="Books"|testing$cats.4=="Books"|testing$cats.5=="Books"|  testing$cats.6=="Books")
testing$FoodandDrink=as.numeric(testing$cats.1=="Food and Drink"|testing$cats.2=="Food and Drink"|testing$cats.3=="Food and Drink"|testing$cats.4=="Food and Drink"|testing$cats.5=="Food and Drink"|  testing$cats.6=="Food and Drink")
testing$DataSource=as.numeric(testing$cats.1=="Data Source"|testing$cats.2=="Data Source"|testing$cats.3=="Data Source"|testing$cats.4=="Data Source"|testing$cats.5=="Data Source"|  testing$cats.6=="Data Source")
testing$WebTech=as.numeric(testing$cats.1=="Web/Tech"|testing$cats.2=="Web/Tech"|testing$cats.3=="Web/Tech"|testing$cats.4=="Web/Tech"|testing$cats.5=="Web/Tech"|  testing$cats.6=="Web/Tech")


# export cleaned
cs=c(1:5,17:29)
write.csv(testing[,cs], file="cleanedmrdata.csv",row.names=FALSE)

