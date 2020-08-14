import sqlite3


def checkhandlepresence(handle):
    """
    Checks to see if the specified handle is in the useraccount table
    :param handle: twitter handle to parse
    :return: boolean: True if handle is in database
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT handle FROM useraccounts WHERE handle=?', (handle, ))
    present = cursor.fetchone()
    conn.close()
    if present is None:
        return False
    else:
        return True


def populateaccountdata(accountdata):
    """
    Populates the database with account data for the specified handle
    :param accountdata: tuple containing downloaded account data
    :return:
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO useraccounts (handle, name_actual, num_followers, num_friends, num_tweets, creation_date) VALUES (?, ?, ?, ?, ?, ?)', accountdata)
    conn.commit()
    conn.close()


def populatetweetdata(tweetdata):
    """
    Populates the database with account data for the specified handle
    :param tweetdata: list of tuples containing downloaded tweet data
    :return:
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT OR IGNORE INTO tweetdata (handle, id, created_at, tweettext_raw, num_retweets, num_favourites) VALUES (?, ?, ?, ?, ?, ?)', tweetdata)
    conn.commit()
    conn.close()


def latesttweetid(handle):
    """
    :param handle: twitter handle of user to find latest tweet id
    :return: integer of the latest tweet id to use for since_id
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM tweetdata WHERE handle=?', (handle, ))  #
    idlist = cursor.fetchall()
    conn.close()
    tweetids = []
    for tuple in idlist:
        tweetids.append(tuple[0])
    return max(tweetids)


def grabaccountdata(handle):
    """
    :param handle: users twitter handle
    :return: a tuple containing account data for a specified handle
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM useraccounts WHERE handle=?', (handle, ))  #
    userdata = cursor.fetchall()[0]
    conn.close()
    return userdata


def grabusertweets(handle):
    """
    :param handle: users twitter handle
    :return: a list of tuples containing all tweets for the specified handle
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tweetdata WHERE handle=?', (handle, ))
    tweets = cursor.fetchall()
    conn.close()
    return tweets
