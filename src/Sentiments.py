from pprint import pprint
import nltk
import yaml
import sys
import os
import re
import json
import functionDefinitions

class Extract_Tweets(): 

    def load_data(): 
        json_2013 = 'gg2013.json'
        json_data_2013 = open(json_2013)
        data_13 = json.load(json_data_2013)
        json_data_2013.close()

        num_of_tweets = len(data_13)

        print "num_of_tweets", num_of_tweets 

        tweets = [] 
        #extract all the text from tweets 
        for i in range (0,num_of_tweets):
            tweets.append(data_13[i]["text"])

        print tweets[100] 

        json_data_2013.close()

        return tweets 

class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    # Returns tokenized sentences 
    def split(self, text):
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences

class POSTagger(object):

    def __init__(self):
        pass
        
    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
          """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])


def sentimentEntryPoint(tweets):

    #tweets = [] 
    #raw_tweets = functionDefinitions.jsonParser('gg2013.json')
    #data_13 = functionDefinitions.filterTweets(raw_tweets)
    data_13 = tweets
    num_of_tweets = len(data_13)
    
    host_positive = [] 
    host_negative = [] 
    winner_pos = []
    winner_neg = []

    category1_pos = []
    category1_neg = [] 

    director_pos = []
    director_neg = [] 

    miniSeries_pos = [] 
    miniSeries_neg = [] 

    actorDrama_pos = []
    actorDrama_neg = [] 

    actorComedy_pos = []
    actorComedy_neg = [] 

    screenplay_p = []
    screenplay_n = []

    #Best supporting actress 
    actress_tvseries_p = []
    actress_tvseries_n = []

    movieDrama_p = [] 
    movieDrama_n = []

    movieComedy_p = []
    movieComedy_n = []

    #extract all the text from tweets 
    #print "Analyzing tweets."
    #print "This might take some time! "
    for i in range (0,num_of_tweets):
        
        text = data_13[i]

        splitter = Splitter()
        postagger = POSTagger()
        dicttagger = DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml', 
                                    'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])

        splitted_sentences = splitter.split(text)

        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
            #pprint(pos_tagged_sentences)
        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
            #pprint(dict_tagged_sentences)

        score = sentiment_score(dict_tagged_sentences)
        #print "###SCORE###", score 

        if score > 0: 
            if(functionDefinitions.find_one_host(text)): 
                host_positive.append(text)
            if (functionDefinitions.lookup_winner(text)):
                winner_pos.append(text)
            if(functionDefinitions.lookup_best_movie_drama(text)):
                category1_pos.append(text)

            if(functionDefinitions.lookup_best_dir(text)):
                director_pos.append(text)

            if(functionDefinitions.lookup_best_actorDrama(text)):
                actorDrama_pos.append(text)

            if(functionDefinitions.lookup_best_actorComedy(text)):
                actorComedy_pos.append(text)

            if(functionDefinitions.lookup_best_screenPlay(text)):
               screenplay_p.append(text)

            if(functionDefinitions.lookup_best_seriesActress(text)):
               actress_tvseries_p.append(text)

            if(functionDefinitions.lookup_best_MovieDrama(text)):
               movieDrama_p.append(text)

            if(functionDefinitions.lookup_best_MovieComedy(text)):
               movieComedy_p.append(text)

        if score < 0: 
            extract_host = Extract_Tweets() 
            if(functionDefinitions.find_one_host(text)): 
                host_negative.append(text)
            if (functionDefinitions.lookup_winner(text)):
                winner_neg.append(text)
            if(functionDefinitions.lookup_best_movie_drama(text)):
                category1_neg.append(text)
            if(functionDefinitions.lookup_best_dir(text)):
                director_neg.append(text)

            if(functionDefinitions.lookup_best_actorDrama(text)):
                actorDrama_neg.append(text)
            if(functionDefinitions.lookup_best_screenPlay(text)):
               screenplay_n.append(text)

            if(functionDefinitions.lookup_best_seriesActress(text)):
               actress_tvseries_n.append(text)

            if(functionDefinitions.lookup_best_MovieDrama(text)):
               movieDrama_n.append(text)

            if(functionDefinitions.lookup_best_MovieComedy(text)):
               movieComedy_n.append(text)


        h_p = len(host_positive)
        h_n = len(host_negative)
        w_p = len(winner_pos)
        w_n = len(winner_neg)
        
        c1_p = len(category1_pos)
        c1_n = len(category1_neg)

        dir_p = len(director_pos)
        dir_n = len(director_neg)

        mini_p = len(miniSeries_pos) 
        mini_n = len(miniSeries_neg)

        act_drama_p = len(actorDrama_pos) 
        act_drama_n = len(actorDrama_neg)


        act_comedy_p = len(actorComedy_pos) 
        act_comedy_n = len(actorComedy_neg)

        sp_p = len(screenplay_p) 
        sp_n = len(screenplay_n)

        atvs_p = len(actress_tvseries_p)
        atvs_n = len(actress_tvseries_n)

        md_p = len(movieDrama_p)
        md_n = len(movieDrama_n)

        mc_p = len(movieComedy_p)
        mc_n = len(movieComedy_n)

        if h_p > 10 or h_n > 10: 
             break 
             
    if (h_p > h_n): 
        print "---------------------------------------------------------------"
        print "The Audience loved the hosts!!!"
        print "---------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in host_positive[5:10]: 
            print x

    else: 
        print "---------------------------------------------------------------"
        print "The Audience Hated the hosts!!!"
        print "---------------------------------------------------------------"
        print "some of the negative  tweets: " 
        for x in host_negative[0:5]: 
            print x

    if (w_p > w_n): 
        print "-------------------------------------------------------------"
        print "The Audience had a positive reaction towards the winners!!!"
        print "-------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in winner_pos[10:30]: 
            print x
    else: 
        print "-------------------------------------------------------------"
        print "The Audience had a negative reaction towards the winners!!!"
        print "-------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in winner_neg[10:30]: 
            print x


    if (c1_p > c1_n): 
        print "-----------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Motion Picture!!"
        print "------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in category1_pos[0:3]: 
            print x
    else: 
        print "--------------------------------------------------------------------"
        print "The Audience had a negative reaction towards Best Motion Picture!!"
        print "-------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in category1_neg[1:5]: 
            print x

    if (dir_p > dir_n): 
        print "-----------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Director!!"
        print "------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in director_pos[0:3]: 
            print x
    else: 
        print "-------------------------------------------------------------"
        print "The Audience had a negative reaction towards the Best Director!!!"
        print "-------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in director_neg[1:5]: 
            print x

    if (act_drama_p > act_drama_n): 
        print "-----------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Actor, Drama!"
        print "------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in actorDrama_pos[0:3]: 
            print x
    else: 
        print "-------------------------------------------------------------------"
        print "The Audience had a negative reaction towards the Best Actor, Drama!!!"
        print "--------------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in actorDrama_neg[0:3]: 
            print x

    if (act_comedy_p > act_comedy_n): 
        print "-----------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Actor, Comedy!"
        print "------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in actorComedy_pos[0:3]: 
            print x
    else: 
        print "-------------------------------------------------------------------"
        print "The Audience had a negative reaction towards the Best Actor, Comedy!!!"
        print "--------------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in actorComedy_neg[0:3]: 
            print x

    if (sp_p > sp_n): 
        print "-----------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Screen Play!"
        print "------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in screenplay_p[0:3]: 
            print x
    else: 
        print "-------------------------------------------------------------------"
        print "The Audience had a negative reaction towards the Best ScreenPlay!!!"
        print "--------------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in screenplay_n[0:3]: 
            print x

    if (atvs_p > atvs_n): 
        print "----------------------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Supporting Actress!!!"
        print "-----------------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in actress_tvseries_p[0:3]: 
            print x
    else: 
        print "---------------------------------------------------------------------------------"
        print "The Audience had a negative reaction towards the  Best Supporting Actress!!!"
        print "---------------------------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in actress_tvseries_n[0:3]: 
            print 

    if (md_p > md_n): 
        print "----------------------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Movie Drama"
        print "-----------------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in movieDrama_p[0:3]: 
            print x
    else: 
        print "---------------------------------------------------------------------------------"
        print "The Audience had a negative reaction towards the Best Movie Drama!"
        print "---------------------------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in movieDrama_n[0:3]: 
            print x

    if (mc_p > mc_n): 
        print "----------------------------------------------------------------------------"
        print "The Audience had a positive reaction towards Best Movie Comedy!"
        print "-----------------------------------------------------------------------------"
        print "some of the positive tweets: " 
        for x in movieComedy_p[0:3]: 
            print x
    else: 
        print "---------------------------------------------------------------------------------"
        print "The Audience had a negative reaction towards the Best Movie Comedy!"
        print "---------------------------------------------------------------------------------"
        print "some of the negative tweets: " 
        for x in movieComedy_n[0:3]: 
            print x
