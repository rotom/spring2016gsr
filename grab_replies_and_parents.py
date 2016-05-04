from TwitterSearch import *
from pprint import *

replies = []
replies_with_parents = [] #this could be a dictionary if we don't want the keys
                          #to be the json representation of a tweet

def get_parent(tweet):
        
    parent_user = tweet['in_reply_to_screen_name']
    parent_id = tweet['in_reply_to_status_id']
    tuo = TwitterUserOrder(parent_user)
    
    try:
        for parent in ts.search_tweets_iterable(tuo):
            if parent['id'] == parent_id:
                print 'PARENT: %s \nREPLY: %s' % (parent['text'], tweet['text'])
                replies_with_parents.append((tweet, parent))
    except Exception as e:
##        if e.code == 401:
##            print parent_user, parent_id, e
##        elif e.code == 429:
##            print e #todo: wait for 15 minutes
##            return
##        else:
##            print e
        print parent_user, parent_id, e


if __name__ == '__main__':
    
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['that sucks']) #each keyword is a case/punctuation-insensitive substring
        tso.set_language('en') #filter non-English tweets
        tso.set_include_entities(False) # and don't give us all those entity information

        # initiate TwitterSearch with appropriate tokens
        ts = TwitterSearch(
            consumer_key = "rifiWQ3JJjo3nrVuA6iM7meX7",
            consumer_secret = "0wjfcoglnnqkV0tJYSLTSvWn7RZpr1HEzmgmwFFjFCDWZBMxee",
            access_token = "24338827-IDwBZtWIlCrhqOyhy9016wbEKdLkxoFuhJI6USPya",
            access_token_secret = "ADkraKk76XI9ESTtyQ2jcTvPrJparDzItJcyO0LHOiQ0D"
         )

        #seed replies
        for tweet in ts.search_tweets_iterable(tso):
            if tweet['in_reply_to_status_id'] != None:
                if len(replies) > 100:
                    break
                replies.append(tweet)
        
        for reply in replies:
            get_parent(reply)

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
