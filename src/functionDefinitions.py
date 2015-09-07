import json
import nltk
import re
from nltk.util import ngrams
import HTMLParser

#for debugging purposes only
from pprint import pprint
import pdb

# Method to parse the JSON file
# Input: path to json file
# Returns: the parsed data in an array 
def jsonParser(path):
    json_data = open(path)
    data = json.load(json_data)
    numOfTweets = len(data)
    tweets = []
    for tweetIndex in range (0,numOfTweets):
        tweets.append(data[tweetIndex]["text"])
    json_data.close()
    return tweets
#function jsonParser end

# to be used to tokenize words in a sentence
from nltk.tokenize import TreebankWordTokenizer
wordTokenizer = TreebankWordTokenizer() 

# to be used to tokenize sentences in a tweet
sentenceTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#import all the stop words
from nltk.corpus import stopwords
stop = stopwords.words('english')

# reg ex for filtering the tweets.
filterRegExPatterns = ['host?[s]', 'hosting', 'hosted', 'won best', 'winner', 'wins', 'presented', 'presenting', 'red carpet', 'best dressed', 'best dress', 
'worst dressed', 'worst dress'] 
filterRegExPatternJoin = "|".join(filterRegExPatterns)
filterRegEx = re.compile(filterRegExPatternJoin, re.IGNORECASE)
#re ex for removing all the retweets
filterRetweetRegEx = re.compile('^RT', re.IGNORECASE)

# Method to filter the tweets, removing tweets that do not make sense
# Input: unfiltered tweets
# Output: filtered tweets 
def filterTweets(tweets):
    filteredTweets = []
    count = 0
    for tweet in tweets:
        if(filterRegEx.search(tweet) and not filterRetweetRegEx.search(tweet)):
            count += 1
            tweetCleaned = re.sub(r'[^a-zA-Z0-9 ]',r'',tweet)
            filteredTweets.append(tweetCleaned)           
    return filteredTweets
#function filterTweets end


# a list of tokens to be removed from the tweets/sentences under analysis
blacklistWords = ['golden', 'globes', 'goldenglobes', '#goldenglobes', '#golden']

#reg ex pattern for filtering tweets with information about the host(s)
hostRegExPatterns = ['host?[s]', 'hosting', 'hosted']
hostRegExPatternJoint = '|'.join(hostRegExPatterns)
hostRegEx = re.compile(hostRegExPatternJoint, re.IGNORECASE)
# a dictionary to store all the probable host names.
hostName = dict()
#list of hosts, formed after manipulating the hostName dictionary
hosts = []

#Method to increase the frequency of a given key, in the dictionary
#INPUT: key to be increased, dictionaryObject: dictionary to refer to, should be global
def addToDictionary(key, dictionaryObject):
    if key in dictionaryObject:
        dictionaryObject[key] += 1
    else:
        dictionaryObject[key] = 1    

#Method to find the most frequently occuring key in a dictionary
#INPUT: dictionary on which to operate, resultList: list contaning the most frequent key value
def findMaxInDictionary(dictionaryObject, resultList):
    max = 0
    for key in dictionaryObject:
        if max < dictionaryObject[key]:
            max = dictionaryObject[key]
    for key in dictionaryObject:
        if max == dictionaryObject[key]:
            resultList.append(key)        

#Method to find the hosts
#INPUT: tweets
def findHost(tweets):
    name = ''
    tweetsScanned = 0
    for tweet in tweets:
        if hostRegEx.search(tweet):
            tweetsScanned += 1
            #remove all stop words and black listed words
            filterText = ' '.join(word for word in tweet.split() if word.lower() not in stop and word.lower() not in blacklistWords)
            unigram = wordTokenizer.tokenize(filterText)
            for bigram in nltk.bigrams(unigram):
                noun = 0
                posTag = nltk.pos_tag(bigram)
                for(data, tag) in posTag:
                    #Check for proper nouns
                    if tag == 'NNP':
                        noun += 1
                #if both the words in bigram are proper nouns, mark the bigram as probable host name        
                if noun == 2:
                    name = "%s %s" % bigram
                    addToDictionary(name, hostName)
        # 10 tweets on hosts are enough to get their names. This can be changed at the cost of processing time.            
        if tweetsScanned > 10:
            break                    
    findMaxInDictionary(hostName, hosts)

# import all the information about the nominees, categories, and regular expressions for each category
import WinnersData
winnerRegEx = WinnersData.winnerRegEx
nomineesByCategory = WinnersData.nomineesByCategory
categories = WinnersData.categories
#regularAwardRegExReordered = WinnersData.regularAwardRegExReordered

# a list to store all the winners. The index will match the category.
# if index 0 represents Best Actor in categories, then the same index in winners list will represent the winner    
winners = []

#Method to find the winners
#INPUT: tweets, nominees indexed according to categories
def findWinners(tweets, nominees_categorized):
    # a dictionary to store all the probable winners for a category, tentatively
    winnerngramList = dict()
    for categoryIndex in range(0, len(categories)):
        for tweet in tweets:
            #Apply the reg ex for the current category
            if winnerRegEx[categoryIndex].search(tweet):
                text = ' '.join(word for word in tweet.split() if word.lower() not in stop and word.lower() not in blacklistWords)
                #After removing stop words, create unigrams from the tweet
                unigrams = wordTokenizer.tokenize(text)
                for unigram in unigrams:
                    # if unigram exists in nominees, the nominee is probably the winner.
                    # words like the, a have been removed. We will mostly end up checking Proper/Common Nouns
                    for nominee in nominees_categorized[categoryIndex]:
                        if unigram in nominee:
                            if nominee in winnerngramList:
                                winnerngramList[nominee] +=1
                            else:
                                winnerngramList[nominee] = 1 
        # of all the probable winners, find the nominee occuring most frequently in the dictionary and mark him/her as winner
        max = 0        
        for key in winnerngramList:
            if(winnerngramList[key] > max):
                max = winnerngramList[key]
        if max == 0:
            winners.append("Data not found")        
        for key in winnerngramList:
            if(winnerngramList[key] == max):
                winners.append(key)   
        winnerngramList.clear()     


#import all the data for special awards - categories and regex for each category
specialAwards = WinnersData.specialCategories
specialAwardsRegEx = WinnersData.specialAwardsRegExReordered

# list containing the special award winners, one for each category
specialAwardWinners = []
# dictionary containing all probable winners of a special award
specialAwardWinner = dict()

# Method to find winners of special awards
# Its implementation is similar to the method to find hosts
def findWinnersSpecialAward(tweets):
    for index in range(0, len(specialAwards)):
        specialAwardStopWords = wordTokenizer.tokenize(specialAwards[index])
        for tweet in tweets:
            if specialAwardsRegEx[index].search(tweet):
                filteredSentences = ' '.join(word for word in tweet.split() if word.lower() not in stop and word.lower() not in blacklistWords 
                    and word not in specialAwardStopWords)
                unigrams = wordTokenizer.tokenize(filteredSentences)
                for bigram in nltk.bigrams(unigrams):
                    posTags = nltk.pos_tag(bigram)
                    noun = 0
                    for (data, tag) in posTags:
                        if tag == 'NNP':
                            noun += 1
                    if noun == 2:
                        name = "%s %s" % bigram
                        addToDictionary(name, specialAwardWinner)                   
        findMaxInDictionary(specialAwardWinner, specialAwardWinners)
        specialAwardWinner.clear()


# Regexes for finding tweets that talk about presenters
presentersRegexPatternList = ['[A-Z][a-z]+ [A-Z][a-z]+ presented', '[A-Z][a-z]+ [A-Z][a-z]+ presenting']
presentersRegexPattern = "|".join(presentersRegexPatternList)
presentersRegEx = re.compile(presentersRegexPattern)

unigramRegExPatternList = ['[A-Z][a-z]+', 'and', 'amp']
unigramRegExPattern = '|'.join(unigramRegExPatternList)
unigramRegEx = re.compile('[A-Z][a-z]+')

best = ["best"]
#dictionary of probable presenters
presentersAward = dict()
# a final list of presenters
presenters = []

# Method to get presenters from a dictionary of probable presenters
# If a name occurs less than once or has more than two words, discard the name
def manipulateDictionary(dictionary):
    for key in dictionary:
        token = wordTokenizer.tokenize(key)
        if dictionary[key] > 1:
            presenters.append(key)       
        elif len(token) ==2:
            presenters.append(key) 

# Method to link an award with presenter(s)
# For each presenter, iterate through each tweet, and use reg ex for award categories
# to find out which category the presenter presented the award for
# The number of tweets talking about presenters boils down to 60-70. So, the number of iterations can be 
# ignored for sake of accuracy.
def linkPresenters(tweets):
     found = 0
     for presenter in presenters:
        for tweet in tweets:
            if presentersRegEx.search(tweet):
                if presenter in tweet:
                    for regexIndex in range(0, len(winnerRegEx)):
                        if winnerRegEx[regexIndex].search(tweet):
                            presentersAward[presenter] = categories[regexIndex]
                    for regexIndex in range(0, len(specialAwardsRegEx)):
                        if specialAwardsRegEx[regexIndex].search(tweet):
                            presentersAward[presenter] = specialAwards[regexIndex]            

# Method to find the presenters
def findPresenters(tweets):
    presentersList = dict()
    for tweet in tweets:
        if presentersRegEx.search(tweet):
            Tweet = re.sub(r'and',r'conjunction', tweet)
            subTweet = re.sub(r'amp',r'conjunction', Tweet)
            filteredSentences = ' '.join(word for word in subTweet.split() if word.lower() not in stop and word.lower() not in blacklistWords)
            unigrams = wordTokenizer.tokenize(filteredSentences)
            name = ''
            for unigram in unigrams:
                if unigram == "presented" or unigram == "presenting":
                    if name != '':
                        if name in presentersList:
                            presentersList[name] += 1
                        else:
                            presentersList[name] = 1 
                    break
                elif  unigramRegEx.search(unigram):
                    name += unigram
                    name += ' '
                elif unigram == "conjunction":
                    if name in presentersList:
                        presentersList[name] += 1
                    else:
                        presentersList[name] = 1 
                    name = ''                             
    manipulateDictionary(presentersList)
    linkPresenters(tweets)

regExRedCarpet = re.compile('red carpet', re.IGNORECASE)
    
regExBestDressPatternList = ['best dress', 'best dressed']
regExBestDressPatterns = '|'.join(regExBestDressPatternList)
regExBestDress = re.compile(regExBestDressPatterns, re.IGNORECASE)

regExWorstDressPatternList = ['worst dress', 'worst dressed']
regExWorstDressPatterns = '|'.join(regExWorstDressPatternList)
regExWorstDress = re.compile(regExWorstDressPatterns, re.IGNORECASE)

regExRivalriesPatternList = ['vs', 'vs.', 'versus', 'against']
regExRivalriesPatterns = '|'.join(regExRivalriesPatternList)
regExRivalries = re.compile(regExRivalriesPatterns, re.IGNORECASE)

wordsToIgnoreRedCarpet = ["best", "dressed", "worst", "dress", "red", "carpet", "photos", "pics", "video", "award", "awards", "celebs",
"celebreties", "celebrity", "dresses", "see", "look", "stole", "stunning"] 

bestDressedList = []
worstDressedList = []
mostTalkedAboutList = []
rivalriesList = []

def getTopN(dictionaryObject, list, n):
    for count in range(0,n):
        maxKey = ''
        max = 0
        for key in dictionaryObject:
            if (dictionaryObject[key] > max):           
                max = dictionaryObject[key]
                maxKey = key
        list.append(maxKey)
        dictionaryObject.pop(maxKey)        


def getRedCarpetInfo(tweets):
    bestDressed = dict()
    worstDressed = dict()
    mostTalkedAbout = dict()
    rivalries = dict()
    for tweet in tweets:
        if regExRivalries.search(tweet):
            filteredSentences = ' '.join(word for word in tweet.split() if word.lower() not in stop and word.lower() not in blacklistWords
                and word.lower() not in wordsToIgnoreRedCarpet)
            unigrams = wordTokenizer.tokenize(filteredSentences)
            for bigram in nltk.bigrams(unigrams):
                    posTags = nltk.pos_tag(bigram)
                    noun = 0
                    for (data, tag) in posTags:
                        if tag == 'NNP':
                            noun += 1
                    if noun == 2:
                        name = "%s %s" % bigram
                        addToDictionary(name, rivalries)                
        if regExBestDress.search(tweet):
            filteredSentences = ' '.join(word for word in tweet.split() if word.lower() not in stop and word.lower() not in blacklistWords
                and word.lower() not in wordsToIgnoreRedCarpet)
            unigrams = wordTokenizer.tokenize(filteredSentences)
            for bigram in nltk.bigrams(unigrams):
                    posTags = nltk.pos_tag(bigram)
                    noun = 0
                    for (data, tag) in posTags:
                        if tag == 'NNP':
                            noun += 1
                    if noun == 2:
                        name = "%s %s" % bigram
                        addToDictionary(name, bestDressed)
        if regExWorstDress.search(tweet):
            filteredSentences = ' '.join(word for word in tweet.split() if word.lower() not in stop and word.lower() not in blacklistWords 
                and word.lower() not in wordsToIgnoreRedCarpet)
            unigrams = wordTokenizer.tokenize(filteredSentences)
            for bigram in nltk.bigrams(unigrams):
                    posTags = nltk.pos_tag(bigram)
                    noun = 0
                    for (data, tag) in posTags:
                        if tag == 'NNP':
                            noun += 1
                    if noun == 2:
                        name = "%s %s" % bigram
                        addToDictionary(name, worstDressed)                
    getTopN(bestDressed, bestDressedList, 5)                    
    getTopN(worstDressed, worstDressedList, 5)
    getTopN(rivalries, rivalriesList, 2)
              
                        

# The following functions are for Sentiment analysis: 

def find_one_host(tweet):
    hostRegEx = re.compile('hosting', re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)):
        # filter the sentences based on the reg ex for host
        result = hostRegEx.search(sentence[sentenceIndex])
        if result:
            return True 

def lookup_winner(tweet):
    winnerngramList = dict()
    # each category 
    for categoryIndex in range(0, len(winnerRegEx)):
        #maxWordCount = GetMaxWordCount(nomineesByCategory[categoryIndex])
        #for index in range(0, len(tweets)):
        result = winnerRegEx[categoryIndex].search(tweet)
        if result:
            return True 


def lookup_best_movie_drama(tweet): 
    winnerngramList = dict() 
    bestMovieDramaRegExPatterns = re.compile('best picture.*drama',re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestMovieDramaRegExPatterns.search(sentence[sentenceIndex])
        if result: 
            return True 

def lookup_best_dir(tweet):
    winnerngramList = dict() 
    bestDirectorRegEx = re.compile('best director', re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestDirectorRegEx.search(sentence[sentenceIndex])
        if result: 
            return True 


def lookup_best_miniSeries(tweet):
    winnerngramList = dict() 
    bestMiniSeriesRegEX = re.compile('best mini.*series', re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestMiniSeriesRegEX.search(sentence[sentenceIndex])
        if result: 
            return True 

def lookup_best_actorDrama(tweet):
    winnerngramList = dict() 
    bestActorDramaRegEx = re.compile('best actor.*drama', re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestActorDramaRegEx.search(sentence[sentenceIndex])
        if result: 
            return True 


def lookup_best_actorComedy(tweet):
    winnerngramList = dict() 
    bestActorComedyRegEx = re.compile('best actor.*comedy', re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestActorComedyRegEx .search(sentence[sentenceIndex])
        if result: 
            return True 

def lookup_best_screenPlay(tweet):
    winnerngramList = dict() 
    bestScreenplayRegEx = re.compile('best screenplay', re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestScreenplayRegEx.search(sentence[sentenceIndex])
        if result: 
            return True 

def lookup_best_animated(tweet):
    bestAnimatedFilmRegExPatterns = ['best animated film', 'best animated movie']
    bestAnimatedFilmPattern = '|'.join(bestAnimatedFilmRegExPatterns)
    bestAnimatedFilmRegEX = re.compile(bestAnimatedFilmPattern, re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestAnimatedFilmRegEX.search(sentence[sentenceIndex])
        if result: 
            return True 
            

def lookup_best_seriesActress(tweet): 
    bestSupportingActressRegExPatterns = ['best supporting actress', 'best actress.*supporting']
    bestSupportingActressPattern = '|'.join(bestSupportingActressRegExPatterns)
    bestSupportingActressRegEx = re.compile(bestSupportingActressPattern, re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result =  bestSupportingActressRegEx.search(sentence[sentenceIndex])
        if result: 
            return True  

def lookup_best_MovieDrama(tweet):
    bestMovieDramaRegExPatterns = ['best picture.*drama', 'best motion picture.*drama', 'best movie.*drama']
    bestMovieDramaPattern = '|'.join(bestMovieDramaRegExPatterns)
    bestMovieDramaRegEx = re.compile(bestMovieDramaPattern, re.IGNORECASE)
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestMovieDramaRegEx.search(sentence[sentenceIndex])
        if result: 
            return True  

def lookup_best_MovieComedy(tweet): 
    bestMovieComedyRegExPatterns = ['best picture.*comedy', 'best motion picture.*comedy', 'best movie.*comedy']
    bestMovieComedyPattern = '|'.join(bestMovieComedyRegExPatterns)
    bestMovieComedyRegEx = re.compile(bestMovieComedyPattern, re.IGNORECASE)   
    sentence = sentenceTokenizer.tokenize(tweet)
    for sentenceIndex in range (0, len(sentence)): 
        result = bestMovieComedyRegEx.search(sentence[sentenceIndex])
        if result: 
            return True                                           
    
##Sentiment analysis terminates
            


         
            




