import tweepy


def createapi():
    """
    Creates the API variable for twitter functions
    :return: api object
    """
    consumer_key = 'YOURKEY'
    consumer_secret = 'YOURSECRET'
    access_token = 'YOURTOKEN'
    access_token_secret = 'YOURSECRETTOKEN'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth, wait_on_rate_limit=True)


def grabaccountdata(handle, api):
    """
    Collects user account data from the specified handle
    :param handle: a twitter handle string
    :param api: api connection
    :return: a tuple of user account data
    """
    try:
        # create user object and store user account data
        user = api.get_user(handle)

        name_actual = user.name
        numfollowers = user.followers_count
        numfriends = user.friends_count
        numtweets = user.statuses_count
        creationdate = dateonly(str(user.created_at))

        accountdata = (handle, name_actual, numfollowers, numfriends, numtweets, creationdate)
        return accountdata
    except RateError:
        raise str('Twitter or rate limit error. Number of API calls: ' + apicallcount)


def grabtweetdata(handle, api, sinceid):
    """
    Collects initial tweet data from the specified handle
    :param sinceid: specified if onlt new tweets are required
    :param handle: a twitter handle string
    :param api: api connection
    :return: a list of tuples containing tweet data
    """
    if sinceid ==0:
        apicall = tweepy.Cursor(api.user_timeline, id='@' + handle, tweet_mode='extended',
                                   include_rts=False).items()
    else:
        apicall = tweepy.Cursor(api.user_timeline, id='@' + handle, since_id=sinceid, tweet_mode='extended',
                                   include_rts=False).items()

    tweets = []
    try:
        # 3,200 tweet limit applies, even when not including retweets.
        for tweet in apicall:
            tweetdata = tuple()  # tuple must be reinitialised before populating since it is immutable
            id = tweet._json['id_str']
            createdat = tweet._json['created_at']
            tweettext_raw = tweet.full_text
            #  coords = tweet._json['coordinates']
            #  location = tweet._json['place']
            numretweets = tweet._json['retweet_count']
            numfavourites = tweet._json['favorite_count']

            tweetdata = (handle, id, createdat, tweettext_raw, numretweets, numfavourites)
            tweets.append(tweetdata[:])
        return tweets
    except RateError:
        raise str('Twitter or rate limit error.')