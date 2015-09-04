# todo
import csv
import cPickle as pickle
from legacyAnalyzer import getFeatureVector, getStopWordList, processTweet, extract_features
import legacyAnalyzer
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
inpTweets = csv.reader(open(root_path + '/full_training_dataset.csv', 'rb'), delimiter=',', quotechar='"')
stopWords = getStopWordList(root_path + '/feature_list/ultimatestopwords.txt')    
legacyAnalyzer.featureList = []

for row in inpTweets:
    sentiment = row[0]
    trainingTweet = row[1]
    processedTweet = processTweet(trainingTweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    legacyAnalyzer.featureList.extend(featureVector)
# Remove featureList duplicates
featureList = list(set(legacyAnalyzer.featureList))
# clFile = open(root_path + '/trained', "r")
clFile = open(root_path + '/naivebayes_trained_model.pickle', "r")
NBClassifier = pickle.load(clFile)
clFile.close()
# NBClassifier.show_most_informative_features(300)
    
def classifyTweet(tweet):

#     # Generate the training set
#     training_set = nltk.classify.util.apply_features(extract_features, tweets)
#      
#     # Train the Naive Bayes classifier
#     NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
#      
#     clFile = open("classifier", "wb")
#     pickle.dump(NBClassifier, clFile)
#     clFile.close()
    
    # Test the classifier
    # processedTweet = processTweet(tweet)
    # vec = getFeatureVector(processedTweet, stopWords)
    features = extract_features(tweet)
#     print features
    sentiment = NBClassifier.classify(features)
#     print "tweet = %s, sentiment = %s\n" % (tweet, sentiment)
    return sentiment
    
clToScore = {"positive": 4, "neutral": 2, "negative":0}
    
def classifyTweets(tweets):
    
    score = 0
    for tweet in tweets:
        classification = classifyTweet(tweet)
#         print classification
        score += clToScore[classification]
    return score
        
if __name__ == "__main__":
    tweets = []
#     for i in range(100):
#         tweets.append(["great", "food"])
    tweets.append(["really", "awesome"])
    print "started"
    print classifyTweets(tweets)
    print "done"
