import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
       
        consumer_key = '18QHFMz0zvycM2KLrTMfrafI1'
        consumer_secret = 'WNwYGKBXmbfsY7ysZXxPJ4Voa7rgtLxGocuDHbIJ1TZLShtBVF'
        access_token = '843094924299976704-GNJyLjovEGFAiOWLswFBagKxlebRQUq'
        access_token_secret = 'L39Wz6lXKSavutPqhopmNwK7egJiSrwRxVohjbqVqbQvM'
 
       
        try:
         
            self.auth = OAuthHandler(consumer_key, consumer_secret)
         
            self.auth.set_access_token(access_token, access_token_secret)
        
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        
        analysis = TextBlob(self.clean_tweet(tweet))
       
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
       
        tweets = []

        try:
          
            fetched_tweets = self.api.search(q = query, count = count)


            for tweet in fetched_tweets:
               
                parsed_tweet = {
                    'text': tweet.text,
                    'sentiment': self.get_tweet_sentiment(tweet.text),
                }
                 

                if (
                    tweet.retweet_count > 0
                    and parsed_tweet not in tweets
                    or tweet.retweet_count <= 0
                ):
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print(f"Error : {str(e)}")
 
def main():
    api = TwitterClient()
    tweets = api.get_tweets(query = 'Marketing', count = 500)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    print(f"Positive tweets percentage: {100 * len(ptweets) / len(tweets)} %")

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print(f"Negative tweets percentage: {100 * len(ntweets) / len(tweets)} %")

    print(
        f"Neutral tweets percentage: {100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)} % "
    )

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
 
if __name__ == "__main__":

    main()
