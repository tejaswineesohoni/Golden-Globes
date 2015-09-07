# WinnersData.py contains all the reg ex for finding winners for each category.
# It also contains the nominees for each category
import re
import crawler

bestMovieDramaRegExPatterns = ['best.*picture.*drama', 'best.*motion picture.*drama', 'best.*movie.*drama']
bestMovieDramaPattern = '|'.join(bestMovieDramaRegExPatterns)
bestMovieDramaRegEx = re.compile(bestMovieDramaPattern, re.IGNORECASE)
bestMovieComedyRegExPatterns = ['best.*picture.*comedy', 'best.*motion.*picture.*comedy', 'best.*movie.*comedy']
bestMovieComedyPattern = '|'.join(bestMovieComedyRegExPatterns)
bestMovieComedyRegEx = re.compile(bestMovieComedyPattern, re.IGNORECASE)
bestActorDramaRegEx = re.compile('best.*actor.*drama', re.IGNORECASE)
bestActorComedyRegEx = re.compile('best.*actor.*comedy', re.IGNORECASE)
bestActressDramaRegEx = re.compile('best.*actress.*drama', re.IGNORECASE)
bestActressComedyRegEx = re.compile('best.*actress.*comedy', re.IGNORECASE)
bestSupportingActorRegExPatterns = ['best.*supporting.*actor', 'best.*actor.*supporting']
bestSupportingActorPattern = '|'.join(bestSupportingActorRegExPatterns)
bestSupportingActorRegEx = re.compile(bestSupportingActorPattern, re.IGNORECASE)
bestSupportingActressRegExPatterns = ['best.*supporting actress', 'best.*actress.*supporting']
bestSupportingActressPattern = '|'.join(bestSupportingActressRegExPatterns)
bestSupportingActressRegEx = re.compile(bestSupportingActressPattern, re.IGNORECASE)
bestDirectorRegEx = re.compile('best director', re.IGNORECASE)
bestScreenplayRegEx = re.compile('best screenplay', re.IGNORECASE)
bestOriginalSongRegEx = re.compile('best [original]* song', re.IGNORECASE)
bestOriginalScoreRegEx = re.compile('best [original]* score', re.IGNORECASE)
bestForeignLanguageRegEx = re.compile('best foreign language', re.IGNORECASE)
bestAnimatedFilmRegExPatterns = ['best animated film', 'best animated movie']
bestAnimatedFilmPattern = '|'.join(bestAnimatedFilmRegExPatterns)
bestAnimatedFilmRegEX = re.compile(bestAnimatedFilmPattern, re.IGNORECASE)
bestActorTVSeriesDramaRegExPatterns = ['best.*actor.*television series.*drama', 'best.*actor.*tv.*series.*drama']
bestActorTVSeriesDramaPattern = '|'.join(bestActorTVSeriesDramaRegExPatterns)
bestActorTVSeriesDramaRegEX = re.compile(bestActorTVSeriesDramaPattern, re.IGNORECASE)
bestActorMiniSeriesRegEX = re.compile('best.*actor.*mini.*series', re.IGNORECASE)
bestActorTVSeriesComedyRegExPatterns = ['best.*actor.*television.*series.*comedy', 'best.*actor.*tv.*series.*comedy']
bestActorTVSeriesComedyPattern = '|'.join(bestActorTVSeriesComedyRegExPatterns)
bestActorTVSeriesComedyRegEX = re.compile(bestActorTVSeriesComedyPattern, re.IGNORECASE)
bestActressTVSeriesDramaRegExPatterns = ['best.*actress.*television series.*drama', 'best.*actress.*tv series.*drama']
bestActressTVSeriesDramaPattern = '|'.join(bestActressTVSeriesDramaRegExPatterns)
bestActressTVSeriesDramaRegEX = re.compile(bestActressTVSeriesDramaPattern, re.IGNORECASE)
bestActressMiniSeriesRegEX = re.compile('best.*actress.*mini.*series', re.IGNORECASE)
bestActressTVSeriesComedyRegExPatterns = ['best.*actress.*television.*series.*comedy', 'best.*actress.*tv.*series.*comedy']
bestActressTVSeriesComedyPattern = '|'.join(bestActressTVSeriesComedyRegExPatterns)
bestActressTVSeriesComedyRegEX = re.compile(bestActressTVSeriesComedyPattern, re.IGNORECASE)
bestSupportingActorTVSeriesRegExPatterns = ['best.*supporting.*actor.*[tv]*.*[series]*', 'best.*actor.*supporting.*[tv]*.*[series]*']
bestSupportingActorTVSeriesPattern = '|'.join(bestSupportingActorTVSeriesRegExPatterns)
bestSupportingActorTVSeriesRegEx = re.compile(bestSupportingActorTVSeriesPattern, re.IGNORECASE)
bestSupportingActressTVSeriesRegExPatterns = ['best.*supporting.*actress.*[tv]*.*[series]*', 'best.*actress.*supporting.*[tv]*.*[series]*']
bestSupportingActressTVSeriesPattern = '|'.join(bestSupportingActressTVSeriesRegExPatterns)
bestSupportingActressTVSeriesRegEx = re.compile(bestSupportingActressTVSeriesPattern, re.IGNORECASE)
bestTVSeriesComicalRegExPatterns = ['best [television]* series.*[musical or comedy]*']
bestTVSeriesComicalPattern = '|'.join(bestTVSeriesComicalRegExPatterns)
bestTVSeriesComicalRegEx = re.compile(bestTVSeriesComicalPattern, re.IGNORECASE)
bestTVSeriesDramaRegExPatterns = ['best [television]* series.*drama']
bestTVSeriesDramaPattern = '|'.join(bestTVSeriesDramaRegExPatterns)
bestTVSeriesDramaRegEx = re.compile(bestTVSeriesDramaPattern, re.IGNORECASE)
bestMiniSeriesRegEX = re.compile('best mini.*series', re.IGNORECASE)

winnerRegEx = [bestMovieDramaRegEx, bestMovieComedyRegEx, bestActorDramaRegEx, bestActorComedyRegEx,
bestActressDramaRegEx, bestActressComedyRegEx, bestSupportingActorRegEx, bestSupportingActressRegEx, bestDirectorRegEx,
bestScreenplayRegEx, bestOriginalSongRegEx, bestOriginalScoreRegEx, bestForeignLanguageRegEx, bestAnimatedFilmRegEX, bestActorTVSeriesDramaRegEX, bestActorMiniSeriesRegEX,
bestActorTVSeriesComedyRegEX, bestActressTVSeriesDramaRegEX, bestActressMiniSeriesRegEX, bestActressTVSeriesComedyRegEX, bestSupportingActorTVSeriesRegEx,
bestSupportingActressTVSeriesRegEx, bestTVSeriesComicalRegEx, bestTVSeriesDramaRegEx, bestMiniSeriesRegEX]

winnerRegExOrdered = []

nomineesByCategory = []

categories = crawler.categories
specialCategories = crawler.specialCategories

deMilleAwardRegEx = re.compile('cecil.*[b]*.*[demille]*', re.IGNORECASE)
missGoldenGlobeAwardRegEx = re.compile('miss.*golden.*globe', re.IGNORECASE)
specialAwardsRegEx = [deMilleAwardRegEx, missGoldenGlobeAwardRegEx]
specialAwardsRegExReordered = dict()

regularAwardRegExReordered = dict()

def createCategoryNomineeDict(nominees_ByCategory):
	for index in range(0, len(categories)):
		for regEx in winnerRegEx:
			if regEx.search(categories[index]):
				regularAwardRegExReordered[index] = regEx
				break 
	for categoryIndex in range(0, len(specialCategories)):
	 	for regEx in specialAwardsRegEx:
	 		if regEx.search(specialCategories[categoryIndex]):
	 			specialAwardsRegExReordered[categoryIndex] = regEx
	nomineesByCategory = nominees_ByCategory 			
 						

