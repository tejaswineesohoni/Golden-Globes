from bs4 import BeautifulSoup
import urllib2
import re

regExTitle = re.compile("^/title")
regExName = re.compile("^/name")

categoryRegEx = re.compile('^Best', re.IGNORECASE)

categories = []
specialCategories = []

specialCategoryRegEx = re.compile('^golden globe', re.IGNORECASE)

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def crawl(page_url):
	html_page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(html_page)
	winners = [] 
	for header in soup.findAll('h3'):
		if header.text == 'WINNER': 
			divTag = header.findNext('div')
			for strongTag in divTag.findAll('strong'): 
				for hrefTagTitle in strongTag.findAll('a', attrs={'href': regExTitle}):
					titleString = hrefTagTitle.string
					names = strongTag.findNext('a', attrs={'href': regExName})
					if names.string == None:
						winners.append(titleString)
					else:
						team = 	names.string	
						names = names.findNextSiblings('a', attrs={'href': regExName})
						for index in range(0,len(names)):
							team += ", " + names[index].string
						detailedString = team + " for " + titleString
						winners.append(detailedString)

	big_list = [] 
	nominees = [] 
	for header in soup.findAll('h3'):
		if header.text == 'NOMINEES': 
			divTag = header.findNext('div',attrs={'class':'alt'})
			for strongTag in divTag.findAll('strong'): 
				for hrefTagTitle in strongTag.findAll('a', attrs={'href': regExTitle}):
					titleString = hrefTagTitle.string
					names = strongTag.findNext('a', attrs={'href': regExName})
					if names.string == None:
						nominees.append(titleString)
					else:
						team = 	names.string	
						names = names.findNextSiblings('a', attrs={'href': regExName})
						for index in range(0,len(names)):
							team += ", " + names[index].string
						detailedString = team + " for " + titleString
						nominees.append(detailedString)					

			divTag = divTag.findNext('div', attrs={'class':'alt2'})
			for strongTag in divTag.findAll('strong'): 
				for hrefTagTitle in strongTag.findAll('a', attrs={'href': regExTitle}):
					titleString = hrefTagTitle.string
					names = strongTag.findNext('a', attrs={'href': regExName})
					if names.string == None:
						nominees.append(titleString)
					else:
						team = names.string	
						names = names.findNextSiblings('a', attrs={'href': regExName})
						for index in range(0,len(names)):
						 	team += ", " + names[index].string
						detailedString = team + " for " + titleString
						nominees.append(detailedString)
			
			divTag = divTag.findNext('div', attrs={'class':'alt'})
			for strongTag in divTag.findAll('strong'): 
				for hrefTagTitle in strongTag.findAll('a', attrs={'href': regExTitle}):
					titleString = hrefTagTitle.string
					names = strongTag.findNext('a', attrs={'href': regExName})
					if names.string == None:
						nominees.append(titleString)
					else:
						team = names.string	
						names = names.findNextSiblings('a', attrs={'href': regExName})
						for index in range(0,len(names)):
						 	team += ", " + names[index].string
						detailedString = team + " for " + titleString
						nominees.append(detailedString)

			divTag = divTag.findNext('div', attrs={'class':'alt2'})
			for strongTag in divTag.findAll('strong'): 
				for hrefTagTitle in strongTag.findAll('a', attrs={'href': regExTitle}):
					titleString = hrefTagTitle.string
					names = strongTag.findNext('a', attrs={'href': regExName})
					if names.string == None:
						nominees.append(titleString)
					else:
						team = names.string	
						names = names.findNextSiblings('a', attrs={'href': regExName})
						for index in range(0,len(names)):
						 	team += ", " + names[index].string
						detailedString = team + " for " + titleString
						nominees.append(detailedString)

	nominees_categorized = []
	nominees_categorized = list(chunks(nominees, 4))

	for i in range(len(nominees_categorized)): 
		nominees_categorized[i].append(winners[i])

	for header in soup.find_all('h2'):
		headerText = header.text
		if categoryRegEx.search(headerText):
			categories.append(headerText)
			
	for header in soup.find_all('h1'):
		headerText = header.text
		if specialCategoryRegEx.search(headerText):
			continue
		else:
			specialCategories.append(headerText)			

	return nominees_categorized						