import scrape
import twitter
import database
import analysis

handles = scrape.populatehandles()
api = twitter.createapi()

# download tweet data
for handle in handles:
    if not database.checkhandlepresence(handle):  # twitter handle is not already in the database
        accountdata = twitter.grabaccountdata(handle, api)
        database.populateaccountdata(accountdata)
        sinceid = 0
        printstr = 'populated.'
        print('Account data for ' + handle + ' has been successfully populated.')
    else:  # twitter handle has already been scraped
        sinceid = database.latesttweetid(handle)
        printstr = 'updated.'
    tweetdata = twitter.grabtweetdata(handle, api, sinceid)
    database.populatetweetdata(tweetdata)
    print('Tweet data for ' + handle + ' has been successfully ' + printstr)
print("-----------------------------------------------------------------------------------")
print('Twitter scrape completed.')
print('-----------------------------------------------------------------------------------')

#  load data in to object dictionary objects
handle_dictionary = {}
for handle in handles:
    #  load account data and tweets
    accountdata = database.grabaccountdata(handle)
    tweets = database.grabusertweets(handle)

    freqdict_words = {}
    freqdict_hashtags = {}
    freqdict_mentions = {}
    freqdict_emojis = {}
    for tweet in tweets:
        for tweetbody in tweet[3:4]:
            analysis.processtweettext(tweetbody, freqdict_words, freqdict_hashtags, freqdict_mentions, freqdict_emojis)
    handle_dictionary[handle] = (accountdata, freqdict_words, freqdict_hashtags, freqdict_mentions, freqdict_emojis)
print('Object dictionary created.')
print('-----------------------------------------------------------------------------------')
print('Please instantiate an Analyser class using the following command:\n')
print('TWITTERHANDLE = analysis.Analyser(accountdata, freqdict_words, freqdict_hashtags, freqdict_mentions, '
      'freqdict_emojis)\n')
print('Enter \"print(handle_dictionary.keys())\" to see a list of the available twitter handles.\n')
print('The Analyser class arguments is found in the handle_dictionary values. For example, to create an Analyser '
      'class for Barack Obama, the command would be:\n')
print('BarackObama = analysis.Analyser(handle_dictionary.get(\'BarackObama\'))')

