from os import system
import date_features
import datetime

outputFilePath = "./output/snscrape-output.txt"


def downloadTweetUrls(hashtag: str, date: datetime.datetime) -> None:
    """
    Downloads the tweet urls from the specified hashtag at that day into the output file path.
    
    Arguments:
        hashtag: hashtag to search for excluding "#"
        date: date as a datetime object
    """
    system(f'snscrape --progress --since {date_features.formatDate(date)} twitter-hashtag "{hashtag} until:{date_features.formatDate(date_features.getNextDay(date))}" >{outputFilePath}')


def getNumberOfLines(filePath: str) -> int:
    with open(filePath, 'r') as file:
        return len(file.readlines())


def getNumberOfTweets(hashtag: str, date: datetime.datetime) -> int:
    """
    Gets the number of tweets from the specified hashtag at that day.
    
    Arguments:
        hashtag: hashtag to search for excluding "#"
        date: date as a datetime object

    Returns:
        number of tweets (returns -1 if an exception is raised)
    """
    downloadTweetUrls(hashtag, date)
    return getNumberOfLines(outputFilePath)
    

def getPastMonthsNumberOfTweets(hashtag: str) -> list:
    """Gets a list of the number of tweets from the specified hashtag for the past month."""
    pastMonthsNumberOfTweets = []
    for days in range(-30, 1):
        pastMonthsNumberOfTweets.append(getNumberOfTweets(hashtag, date_features.getRelativeDate(days)))
        print(f"Got number of #{hashtag} tweets on {date_features.formatDate(date_features.getRelativeDate(days))}")

    return pastMonthsNumberOfTweets


def getPastDaysOfTheWeek(hashtag: str) -> list:
    """Gets a list of the number of tweets from the specified hashtag for the past 30 days of the specified day of the week (e.g. Tuesday)."""
    return [getNumberOfTweets(hashtag, date_features.getRelativeDate(days)) for days in range(-210, 1, 7)]


def getTodaysPercentile(numberOfTweetsList: list) -> int:
    """(If today has the """
    todaysNumberOfTweets = numberOfTweetsList[-1]
    sortedMonthsNumberOfTweets = numberOfTweetsList.copy()
    sortedMonthsNumberOfTweets.sort()
    minIndex = sortedMonthsNumberOfTweets.index(todaysNumberOfTweets)
    sortedMonthsNumberOfTweets.sort(reverse=True)
    maxIndex = len(numberOfTweetsList) - 1 - sortedMonthsNumberOfTweets.index(todaysNumberOfTweets)
    return round((minIndex + maxIndex) / 2 / .3)


def isTodayTrending(percentile: int) -> bool:
    """
    Returns whether today is above the 90th percentile - whether today is in the to top 3 compared to the last month.
    
    Arguments:
        numberOfTweetsList: list of the number of tweets for the past month or 30 specified days of the week
    """
    return percentile >= 90


def getTodaysStatistics(hashtag: str, standardAlgorithm: bool) -> tuple:
    """
    Arguments:
        hashtag: hashtag to search for excluding "#"
        standardAlgorithm: whether compare today to the past 30 days or the past 30 similar days of the week

    Returns:
        (
            isTodayTrending: bool,
            percentile: int,
            numberOfTweetsList: list
        )
    """
    numberOfTweetsList = getPastMonthsNumberOfTweets(hashtag) if standardAlgorithm else getPastDaysOfTheWeek(hashtag)
    percentile = getTodaysPercentile(numberOfTweetsList)
    return isTodayTrending(percentile), percentile, numberOfTweetsList
