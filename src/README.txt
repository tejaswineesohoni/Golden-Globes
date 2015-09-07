GOLDEN GLOBES PROJECT

Libraries used:
NLTK - for extracting grams and parts of speech tags
RegEx - for using regular expressions
BeautifulSoup - for web scraping

Steps to run the code:
- Run the file main.py
- In command line enter the following when prompted:
“Which edition(year) of the awards are you interested in:” —> Enter (2013 or 2015)
“What trail do I follow to get the tweets:” —> path to the JSON file, path should be in double quotes (“g2013.json”). Note: gg2015.json was too large to upload. You will have to copy it into the src directory.
- The results will be stored in results.json. You can use this as an input to the autograder. 



Notes:
This system is adaptable to any edition(year) of the Golden Globes Awards. This is because all the information is either scraped from the internet or extracted from tweets for a particular year. To be more specific, all nominees and award categories are scraped from the website: 
http://www.imdb.com/event/ev0000292 , which is the IMDB page for Golden Globe Awards. The hosts, award winners and presenters are extracted from the tweets.

A few changes need to be made to ensure that this system adapts to all award ceremonies.
- Change the url mentioned above, if IMDB does not provide information about the other award ceremonies.
- If the url is changed, alter the scraping technique.
- Change the list of black listed words. These are the most commonly occurring words besides the stop words. For example, in our case it is Golden Globes, #goldenglobes, etc. For an award show like Oscars, the words oscars, #oscar, academy awards, will be added to this list.


