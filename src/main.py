import twitter_features
from email_features import sendNotification
from mongodb_features import getSubscriptions


if __name__ == "__main__":
    for subscription in getSubscriptions():
        (
            _,
            email, 
            hashtag, 
            standardAlgorithm,
            dailyEmail
        )  = subscription.values()

        # calculate stats
        numberOfTweetsList = twitter_features.getPastMonthsNumberOfTweets(hashtag) if standardAlgorithm else twitter_features.getPastDaysOfTheWeek(hashtag)
        percentile = twitter_features.getTodaysPercentile(numberOfTweetsList)
        isTodayTrending = twitter_features.isTodayTrending(percentile)

        # potentially send email
        if isTodayTrending or dailyEmail:
            sendNotification(email, hashtag, standardAlgorithm, percentile, numberOfTweetsList)
