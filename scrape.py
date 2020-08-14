import requests
from bs4 import BeautifulSoup


def grabhtmltext(url):
    """
    Grabs the source html code from a webpage.
    :param url: desired webpage to grab html code from
    :return: a string containing the source html code.
    """
    r = requests.get(url)
    htmltext = r.content
    return htmltext


def populatehandles():
    """
    Populates a list of twitter handles of the 50 most popular accounts.
    :return: a list containing the twitter handles without the @ sign
    """

    handles = []
    htmltext = grabhtmltext('https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts')
    soup = BeautifulSoup(htmltext, 'html.parser')
    table = soup.find("table")
    for row in table.find_all("tr")[1:]:
        col = row.find_all("td")
        colstr = str(col[1])
        colstr = colstr.replace('</td>', '')
        if 'href' in colstr:  # if cell contains hyperlink
            colstr = colstr.replace('</a>', '')
        atloc = colstr.find('@')
        handle = colstr[atloc + 1:].rstrip()
        handles.append(handle)
    return handles
