import string
import re

abbreviatedwords = {
    "doesn\'t": ["does", "not"],
    "won\'t": ["can", "not"],
    "don\'t": ["do", "not"],
    "i\'ve": ["i", "have"],
    "i\'d": ["i", "would"],
    "i\'m": ["i", "am"],
    "i\'ll": ["i" "will"],
    "she\'s": ["she", "is"],
    "he\'s": ["he", "is"],
    "it\'s": ["it", "is"],  # not always correct. could be has
    "there\'s": ["there", "is"],
    "they\'re": ["they", "are"],
    "we\'re": ["we", "are"],
    "you\'ve": ["you", "have"],
    "you\'re": ["you", "are"],
    "couldn\'t": ["could", "not"],
    "shouldn\'t": ["should", "not"],
    "wouldn\'t": ["would", "not"],
    "doesn’t": ["does", "not"],
    "won’t": ["can", "not"],
    "don’t": ["do", "not"],
    "i’ve": ["i", "have"],
    "i’d": ["i", "would"],
    "i’m": ["i", "am"],
    "i’ll": ["i" "will"],
    "she’s": ["she", "is"],
    "he’s": ["he", "is"],
    "it’s": ["it", "is"],  # not always correct. could be has
    "there’s": ["there", "is"],
    "they’re": ["they", "are"],
    "we’re": ["we", "are"],
    "you’ve": ["you", "have"],
    "you’re": ["you", "are"],
    "couldn’t": ["could", "not"],
    "shouldn’t": ["should", "not"],
    "wouldn’t": ["would", "not"],
}


def dateonly(datetime):
    """
    Extracts the date from the date and time creation string.
    :param datetime: string containing the date and time of creation from twitter.
    :return: string containing the creation date only
    """

    spaceloc = datetime.find(' ', 0)
    return datetime[:spaceloc]


def tokenise(tweetstring, lowercase=True):
    """
    Splits the raw tweet string in to a sorted list of tokens. Tokens take the form of words,
    punctuation (except @ and #), @ mentions, # tags and URLs.
    :param tweetstring: the full tweet body text.
    :param lowercase: defaulted to True - converts all tokens to lower case where applicable.
    :return: a list of tokens.
    """

    regex_str = [
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    tokens = tokens_re.findall(tweetstring)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


def scrubemojis(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               u"\u2328"
                               u"\u21aa"
                               u"\u2022"
                               u"\u23f1"
                               u"\u23f3"
                               u"\u23f0"
                               u"\u23f2"
                               u"\u20e3"
                               u"\u23ea"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def processtweettext(tweetstring_raw, freqdict_words, freqdict_hashtags, freqdict_mentions, freqdict_emojis):
    """
    processes the tweet data to produce 3 dictionaries: word frequency, hash tag frequency and emoji frequency.
    :param tweetstring_raw: string containing the raw tweet text
    :param freqdict_words: word frequency dictionary
    :param freqdict_hashtags: hash tag frequency dictionary
    :param freqdict_mentions: mention frequency dictionary
    :param freqdict_emojis: emoji frequency dictionary
    :return: 3 modified dictionaries: word frequency, hash tag frequency and emoji frequency
    """
    # extract emojis
    emojis = []
    elset = set(tweetstring_raw)
    tweetstring = scrubemojis(tweetstring_raw)
    elset_noemoji = set(tweetstring)
    emojisset = elset.difference(elset_noemoji)
    for char in tweetstring_raw:
        if char in emojisset:
            emojis.append(char)

    #  replace common apostrophised words
    global abbreviatedwords
    wordlist = tweetstring_raw.lower().split(' ')
    listindex = 0
    listlength = len(wordlist)
    while listindex < listlength:
        for element in wordlist[listindex:]:
            listindex += 1
            if element in abbreviatedwords:
                replacement = abbreviatedwords.get(element)
                while element in wordlist: wordlist.remove(element)
                wordlist.extend(replacement)
                listlength = len(wordlist)
                listindex -= 1
                break
    tweetstring = ' '.join(wordlist)

    tweetlist = tokenise(tweetstring)[:]
    permittedchars = set(string.ascii_letters + '\'')

    hashtags = []
    mentions = []
    listindex = 0
    listlength = len(tweetlist)

    # deal with special character groups
    while listindex < listlength:
        for element in tweetlist[listindex:]:
            listindex += 1

            # extract hashtags
            if str(element)[:1] == '#':
                listindex = tweetlist.index(element)
                hashtags.append(element)
                tweetlist.remove(element)
                listlength = len(tweetlist)
                break

            # extract mentions
            elif str(element)[:1] == '@':
                listindex = tweetlist.index(element)
                mentions.append(element)
                tweetlist.remove(element)
                listlength = len(tweetlist)
                break

            # remove hyphenated words
            elif '-' in str(element):
                listindex = tweetlist.index(element)
                replacement = str(element).split('-')
                while element in tweetlist: tweetlist.remove(element)
                tweetlist.extend(replacement)
                listlength = len(tweetlist)
                break

    # remove prohibited characters and leftover urls
    listindex = 0
    listlength = len(tweetlist)
    while listindex < listlength:
        for element in tweetlist[listindex:]:
            listindex += 1
            elset = set(element)
            if not elset.issubset(permittedchars):
                listindex = tweetlist.index(element)
                while element in tweetlist: tweetlist.remove(element)
                listlength = len(tweetlist)
                break

    # populate frequency dictionary of unique words
    for word in tweetlist:
        if freqdict_words.get(word) is None:
            freqdict_words[word] = 1
        else:
            freqdict_words[word] += 1

    # populate frequency dictionary of unique hashtags
    for tag in hashtags:
        if freqdict_hashtags.get(tag) is None:
            freqdict_hashtags[tag] = 1
        else:
            freqdict_hashtags[tag] += 1

    # populate frequency dictionary of unique mentions
    for mention in mentions:
        if freqdict_mentions.get(mention) is None:
            freqdict_mentions[mention] = 1
        else:
            freqdict_mentions[mention] += 1

    # populate frequency dictionary of unique emojis
    for emoji in emojis:
        if freqdict_emojis.get(emoji) is None:
            freqdict_emojis[emoji] = 1
        else:
            freqdict_emojis[emoji] += 1

    return freqdict_words, freqdict_hashtags, freqdict_mentions, freqdict_emojis


class Analyser():
    analyserobjects = []

    def __init__(self, classdata):
        self.analyserobjects.append(self)
        self.accountdata = classdata[0]

        self.freqdict_words = classdata[1]
        self.freqdict_hashtags = classdata[2]
        self.freqdict_mentions = classdata[3]
        self.freqdict_emojis = classdata[4]

    def grabhandle(self):
        return self.accountdata[0:1]

    def grabname(self):
        return self.accountdata[1:2]

    def followercount(self):
        return self.accountdata[2:3]

    def totaltweets(self):
        return self.accountdata[4:5]

    def createdon(self):
        return self.accountdata[5:6]

    def grabwords(self):
        return self.freqdict_words

    def grabhashtags(self):
        return self.freqdict_hashtags

    def grabmentions(self):
        return self.freqdict_mentions

    def grabemojies(self):
        return self.freqdict_emojis

    def numuniquewords(self):
        return len(self.freqdict_words)

    def numuniquehashtags(self):
        return len(self.freqdict_hashtags)

    def numuniquementions(self):
        return len(self.freqdict_mentions)

    def numuniqueemojies(self):
        return len(self.freqdict_emojis)

    def wordcount(self, word):
        if word in self.freqdict_words:
            output = self.freqdict_words.get(word)
        else:
            output = 'Word not used.'
        return output

    def hashtagcount(self, tag):
        if tag in self.freqdict_hashtags:
            output = self.freqdict_hashtags.get(tag)
        else:
            output = 'Hashtag not used.'
        return output

    def mentioncount(self, at):
        if at in self.freqdict_mentions:
            output = self.freqdict_mentions.get(at)
        else:
            output = 'Mention not used.'
        return output

    def emojicount(self, emoji):
        if emoji in self.freqdict_emojis:
            output = self.freqdict_emojis.get(emoji)
        else:
            output = 'Emoji not used.'
        return output
