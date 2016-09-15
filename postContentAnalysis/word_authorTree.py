import pandas as pd
from sklearn.cross_validation import train_test_split
from nltk.corpus import stopwords # for stopwords (commonly used words to ignore)
import nltk # for stopwords
import re
import numpy as np

postsDF = pd.read_pickle('posts.pkl')

# or i could read csv
# postsDF = pd.read_csv('posts.csv')
# split into test and train 


train, test = train_test_split(postsDF, test_size = 0.2) #creates train and test dataframes 

train = train.reset_index()
test = test.reset_index()
# clean test df so only has author and index
# test = test.drop('author', 1)
test = test.drop('post number', 1)

print test.columns.values


def post_to_words( raw_review ):
    # Function to convert a text to a processed string of words
    # The input is a single string (a raw blog post), and 
    # the output is a single string (a preprocessed blog post)
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


num_text= train["text"].size # number of rows
# a list for clean blog text to go in 
clean_train_text = []

# print train['text']

for i in range( 0, num_text ):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    text=train["text"][i]
    t=post_to_words( text )
    clean_train_text.append(t)
    # print to confirm working every 50 posts
    if( (i+1)%50 == 0 ): 
    	print "text %d of %d\n" % ( i+1, num_text )     


from sklearn.feature_extraction.text import CountVectorizer


vectorizer = CountVectorizer(analyzer = "word",  
                             tokenizer = None,    
                             preprocessor = None, 
                             stop_words = None,   
                             max_features = 5000) 


train_data_features = vectorizer.fit_transform(clean_train_text)

train_data_features = train_data_features.toarray()

print train_data_features.shape

vocab = vectorizer.get_feature_names()
# print vocab


# dist = np.sum(train_data_features, axis=0)
# for tag, count in zip(vocab, dist):
#     print count, tag

from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators = 1000) 
forest = forest.fit( train_data_features, train["author"] )

print test.shape

num_posts = len(test["text"])

clean_test_text = [] 

for i in xrange(0,num_posts):
    if( (i+1) % 1000 == 0 ):
        print "Review %d of %d\n" % (i+1, num_posts)
    clean_post = post_to_words( test["text"][i] )
    clean_test_text.append( clean_post )


test_data_features = vectorizer.transform(clean_test_text)
test_data_features = test_data_features.toarray()

result = forest.predict(test_data_features)

print test.columns.values


output = pd.DataFrame( data={"id":test["index"], "author":result} )

output.to_csv( "Bag_of_Words_model.csv", index=False, quoting=3 )

print sum(output['author']=='Alex Tabarrok')

print sum(test['author']=='Alex Tabarrok')

# print test
