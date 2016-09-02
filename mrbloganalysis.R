testing <- read.csv("~/gittt/marginalrev/cleanedmrdata.csv", comment.char="#")


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
