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



####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
####### Regressions?
####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
reg=lm(testing$numberComments~testing$author+testing$numberofWords+testing$CurrentAffairs+
         testing$Education+testing$Music+testing$Philosophy+testing$PoliticalScience+testing$Science+
         testing$History+testing$Law+testing$Games+testing$Books+
         testing$FoodandDrink+testing$DataSource+testing$WebTech)
summary(reg)

a=lm(testing$numberComments~testing$author)
summary(a)

b=lm(testing$numberComments~testing$author+testing$numberofWords)
summary(b)


####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
# DESCRIPTIVE STATS
####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
mean(testing[testing$author=='Alex Tabarrok',]$numberofWords,na.rm=T)
mean(testing[testing$author=='Tyler Cowen',]$numberofWords,na.rm=T)
sd(testing[testing$author=='Alex Tabarrok',]$numberofWords,na.rm=T)
sd(testing[testing$author=='Tyler Cowen',]$numberofWords,na.rm=T)




####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
# PLOTS
####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
par(mfrow=c(1,1))

names(testing)
plot(testing$time,testing$numberofWords)
hist(testing$numberofWords)

# distribution of post word count
ggplot(testing, aes(testing$numberofWords,colour=testing$author,fill=testing$author)) +
  geom_density(alpha=.1)+
  geom_vline(xintercept = mean(testing$numberofWords,na.rm=T))+
  labs(title = "Distribution of post word count")+
  xlab('Word count')+
  ylab('Density')
  

# word count over time plot
ggplot(testing, aes(testing$time,testing$numberofWords,colour=testing$author))+
  geom_point()+
  xlab('Date')+
  ylab('Word Count')+
  labs(title="Word Count over Time")

#comments over time
ggplot(testing, aes(testing$time,testing$numberComments,colour=testing$author))+
  geom_point()+
  xlab('Date')+
  ylab('Comment Count')+
  labs(title="Comment Count over Time")


# word count v comments. relationship?
ggplot(testing, aes(testing$numberofWords,testing$numberComments))+
  geom_point()+
  xlab('Word Count')+
  ylab('Comment Count')+
  labs(title="Comment Count as a function of Word Count?")+
  geom_smooth(method = "lm", se = FALSE)

x=lm(testing$numberComments~testing$numberofWords)
summary(x)


# boxplot comparing # of comments/ 114 NA in comments
sum(is.na(testing$numberComments)) # boxplot still runs tho
ggplot(testing, aes(testing$author, testing$numberComments,fill = testing$author))+
  geom_boxplot()+
  xlab('Author')+
  ylab('Comment Count')+
  labs(title="Tabarrok posts receive more ~2 more comments, on average")


####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
# TESTS
####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
cowen=testing[testing$author=="Tyler Cowen",]
tabarrok=testing[testing$author=="Alex Tabarrok",]
mean(cowen$numberComments,na.rm = T)
mean(tabarrok$numberComments,na.rm = T)
t.test(cowen$numberComments,tabarrok$numberComments)


####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 
# MACHINE LEARNING
####### ####### ####### ####### 
####### ####### ####### ####### 
####### ####### ####### ####### 

# aim = predict whether given post is cowen or tabarrok
totalPosts=nrow(testing)
CowenPosts=nrow(testing[testing$author=='Tyler Cowen',])
# keep in mind that cowen writes most posts, so  guessing cowen will often make you right
# guess cowen only has error rate of ~10%, so we need to improve on that
1-CowenPosts/totalPosts

#used Megan Risdal's great titanic kaggle notebook to help here. 
str(testing)
set.seed(129)
mice_mod <- mice(testing[, !names(testing) %in% c('title','categories','cats.1','cats.2','cats.3','cats.4','cats.5','cats.6','cats.7','cats.8','cats.9','cats.10','time')], method='rf') 
mice_output <- complete(mice_mod)

# compare imputed data and real data
par(mfrow=c(1,2))
hist(testing$numberComments, freq=F, main='numcomments: Original Data', 
     col='darkgreen', ylim=c(0,0.04))
hist(mice_output$numberComments, freq=F, main='numcomments: MICE Output', 
     col='lightgreen', ylim=c(0,0.04))
#switch plot setup back
par(mfrow=c(1,1))



sum(is.na(testing$numberofWords))
# looks good. lets replace
testing$numberComments<- mice_output$numberComments
# no more NAs!
sum(is.na(testing$numberComments))
testing$numberofWords = mice_output$numberofWords
sum(is.na(testing$numberofWords))

sum(is.na(testing))
# still have 3 NAs. just get rid of rows
testing=na.omit(testing)

# split into testing and training data
# shuffle and then split 80/20 
# shuffle to as to get rid of any time effects.
full = testing[sample(nrow(testing)),]
nrow(full)
#find 20 percent
tesnum=floor(.2*nrow(full))
test <- full[1:tesnum,]
train <- full[(tesnum+1):nrow(full),]

set.seed(754)

rf_model <- randomForest(factor(author) ~ time + numberComments + numberofWords + 
                           CurrentAffairs + Education + Music + 
                           Philosophy + PoliticalScience + Science+
                           History + Law + Games + Books + FoodandDrink+
                           DataSource + WebTech,
                         data = train)

# Show model error
plot(rf_model, ylim=c(0,1))
rf_model
legend('bottom', colnames(rf_model$err.rate), col=1:3, fill=1:3)

# importance
importance    <- importance(rf_model)

# make prediction
prediction <- predict(rf_model, test)

sum(prediction==test$author)/nrow(test)
# compare to all cowen guess
nrow(test[test$author=='Tyler Cowen',])/nrow(test)

sum(prediction==test$author)/nrow(test) - nrow(test[test$author=='Tyler Cowen',])/nrow(test)
# this is the improvement. a 1.6% improvement on just always guessing cowen. 
# this solution drop error from 10% to ~8%

# print to excel
solution <- data.frame(PostID = seq(nrow(test)), author = prediction,realauthor=test$author)
write.csv(solution, file = 'rf_mod_Solution.csv', row.names = F)
