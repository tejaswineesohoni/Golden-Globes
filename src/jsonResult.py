import json
import pdb
from pprint import pprint

from nltk.tokenize import TreebankWordTokenizer
wordTokenizer = TreebankWordTokenizer() 

def findWinner(winnerstring):
    winnerList = [] 
    unigrams = wordTokenizer.tokenize(winnerstring)
    for unigram in unigrams:
        if(unigram == "for"):
            break
        else:    
            winnerList.append(unigram)
    winner = " ".join(winnerList)    
    return winner    



def prepareJson(year, hosts, allWinners, allCategories, allPresenters, allNominees, winners, categories, specialCategories, nominees_categorized, presentersAward):
    data2013 = { 
    "metadata": {
        "year": "",
        "names": {
            "hosts": {
                "method": "detected",
                "method_description": "Filter the tweets based on keywords like 'hosts', 'hosting', 'host', using regular expressions. Further filter by removing all stop words and words like 'Golden Globes' from each tweet. Find all the proper nouns in these tweets and add them to a dictionary. The most frequently occuring Proper Nouns in the dictionary will be the names of the host, since we analyze tweets that have information related to hosts."
                },
            "nominees": {
                "method": "scraped",
                "method_description": "Using the Beautiful Soup library, the nominees were scraped from the website http://www.imdb.com/event/ev0000292/(year). After extracting the nominees, they were saved in a list, in the order of the category they represent. For example, index 1 in the nominees list would correspond to the category at index 1 in the award categories list."
                },
            "awards": {
                "method": "scraped",
                "method_description": "Using the Beautiful Soup library, the award categories were scraped from the website http://www.imdb.com/event/ev0000292/(year). The categories include both regular awards and special awards(like Cecil B. DeMille)."
                },
            "presenters": {
                "method": "detected",
                "method_description": "The tweets were filtered using regular expressions, to look for words like 'presented', 'presenter(s)' and 'gave away'. Stop words and words like 'Golden Globes' were removed from these tweets. All proper nouns were extracted from these tweets and pushed into a dictionary. The name that occured only once or had more than 2 words in it, was judged as a false positive and removed from the dictionary. The remaining names were regarded as probable presenters."    
                }
            },
        "mappings": {
            "nominees": {
                "method": "scraped",
                "method_description": "Since both the nominees and award categories were scraped, the mapping was done simultaneously. The order in which the award categories and nominees were scarpes was similar. Hence, an index in the list contaning award categories can be used to extract nominees for that category, in the nominees list. For example, if index 0 represents the category Best Actor in Drama, the same index in nominees list will return the nominees for this category."
                },
            "presenters": {
                "method": "detected",
                "method_description": "After obtaining a list of probable presenters, we iterated through each presenter name and looked for it in the tweets that talked about presenters. Upon finding a presenter's name in a tweet, we use regular expression to extract the award category from that tweet(if it exists). These regular expressions were earlier used to map an award winner to a category, enabling us to re-use them for mappping a potential presenter to an award category."       
                }
            }            
        },
    "data": {
        "unstructured": {
            "hosts": [],
            "winners": [],
            "awards": [],
            "presenters": [],
            "nominees": []
        },
        "structured": {
            "Best Motion Picture - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Motion Picture - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Motion Picture - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Motion Picture - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Motion Picture - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Motion Picture - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Supporting Role in a Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Supporting Role in a Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Director - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Screenplay - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Original Song - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Original Score - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Foreign Language Film": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Animated Film": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Television Series - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Mini-Series or a Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Television Series - Musical or Comedy": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Television Series - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Mini-Series or a Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Television Series - Musical or Comedy": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Television Series - Musical or Comedy": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Television Series - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Mini-Series or Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            }
        }
    }}

    data2015 = { 
    "metadata": {
        "year": "",
        "names": {
            "hosts": {
                "method": "detected",
                "method_description": "Filter the tweets based on keywords like 'hosts', 'hosting', 'host', using regular expressions. Further filter by removing all stop words and words like 'Golden Globes' from each tweet. Find all the proper nouns in these tweets and add them to a dictionary. The most frequently occuring Proper Nouns in the dictionary will be the names of the host, since we analyze tweets that have information related to hosts."
                },
            "nominees": {
                "method": "scraped",
                "method_description": "Using the Beautiful Soup library, the nominees were scraped from the website http://www.imdb.com/event/ev0000292/(year). After extracting the nominees, they were saved in a list, in the order of the category they represent. For example, index 1 in the nominees list would correspond to the category at index 1 in the award categories list."
                },
            "awards": {
                "method": "scraped",
                "method_description": "Using the Beautiful Soup library, the award categories were scraped from the website http://www.imdb.com/event/ev0000292/(year). The categories include both regular awards and special awards(like Cecil B. DeMille)."
                },
            "presenters": {
                "method": "detected",
                "method_description": "The tweets were filtered using regular expressions, to look for words like 'presented', 'presenter(s)' and 'gave away'. Stop words and words like 'Golden Globes' were removed from these tweets. All proper nouns were extracted from these tweets and pushed into a dictionary. The name that occured only once or had more than 2 words in it, was judged as a false positive and removed from the dictionary. The remaining names were regarded as probable presenters."    
                }
            },
        "mappings": {
            "nominees": {
                "method": "scraped",
                "method_description": "Since both the nominees and award categories were scraped, the mapping was done simultaneously. The order in which the award categories and nominees were scarpes was similar. Hence, an index in the list contaning award categories can be used to extract nominees for that category, in the nominees list. For example, if index 0 represents the category Best Actor in Drama, the same index in nominees list will return the nominees for this category."
                },
            "presenters": {
                "method": "detected",
                "method_description": "After obtaining a list of probable presenters, we iterated through each presenter name and looked for it in the tweets that talked about presenters. Upon finding a presenter's name in a tweet, we use regular expression to extract the award category from that tweet(if it exists). These regular expressions were earlier used to map an award winner to a category, enabling us to re-use them for mappping a potential presenter to an award category."       
                }
            }            
        },
    "data": {
        "unstructured": {
            "hosts": [],
            "winners": [],
            "awards": [],
            "presenters": [],
            "nominees": []
        },
        "structured": {
            "Best Motion Picture - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Motion Picture - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Motion Picture - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Motion Picture - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Motion Picture - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Motion Picture - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Supporting Role in a Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Supporting Role in a Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Director - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Screenplay - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Original Song - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Original Score - Motion Picture": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Foreign Language Film": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Animated Feature Film": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Television Series - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Mini-Series or a Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Television Series - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Television Series - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Mini-Series or a Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Television Series - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Television Series - Comedy or Musical": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Television Series - Drama": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "Best Mini-Series or Motion Picture Made for Television": {
                "nominees": [],
                "winner": "",
                "presenters": []
            }
        }
    }}

    if year == 2013:
        data2013['metadata']['year'] = year
        data2013['data']['unstructured']['hosts'] = hosts
        winnerList = []
        for winner in allWinners:
            winnerName = findWinner(winner)
            winnerList.append(winnerName)  
        data2013['data']['unstructured']['winners'] = winnerList
        data2013['data']['unstructured']['awards'] = allCategories
        data2013['data']['unstructured']['presenters'] = allPresenters
        data2013['data']['unstructured']['nominees'] = allNominees
        unknown = ["unknown"]
        for awardIndex in range(0, 25):
        	presentersList = []
        	data2013['data']['structured'][allCategories[awardIndex]]["nominees"] = nominees_categorized[awardIndex]
        	data2013['data']['structured'][allCategories[awardIndex]]["winner"] = winnerList[awardIndex]
        	for key in presentersAward:
        		if(presentersAward[key] == categories[awardIndex]):
        			presentersList.append(key)
        	if (len(presentersList) == 0):		
        		data2013['data']['structured'][allCategories[awardIndex]]["presenters"] = unknown
        	else:
        		data2013['data']['structured'][allCategories[awardIndex]]["presenters"] = presentersList	
        with open('results.json', 'w') as outfile:
            json.dump(data2013, outfile)
    elif year == 2015:
        data2015['metadata']['year'] = year
        data2015['data']['unstructured']['hosts'] = hosts
        winnerList = []
        for winner in allWinners:
            winnerName = findWinner(winner)
            winnerList.append(winnerName)  
        data2015['data']['unstructured']['winners'] = winnerList
        data2015['data']['unstructured']['awards'] = allCategories
        data2015['data']['unstructured']['presenters'] = allPresenters
        data2015['data']['unstructured']['nominees'] = allNominees
        unknown = ["unknown"]
        for awardIndex in range(0, 25):
            presentersList = []
            data2015['data']['structured'][allCategories[awardIndex]]["nominees"] = nominees_categorized[awardIndex]
            data2015['data']['structured'][allCategories[awardIndex]]["winner"] = winnerList[awardIndex]
            for key in presentersAward:
                if(presentersAward[key] == categories[awardIndex]):
                    presentersList.append(key)
            if (len(presentersList) == 0):      
                data2015['data']['structured'][allCategories[awardIndex]]["presenters"] = unknown
            else:
                data2015['data']['structured'][allCategories[awardIndex]]["presenters"] = presentersList    
        with open('results.json', 'w') as outfile:
            json.dump(data2015, outfile)        