import urllib2
import re
import sys

def getPage(url):
    return urllib2.urlopen(url).read()

def getPageName(page):
    return re.search("<h1 id=\"firstHeading\" class=\"firstHeading\" lang=\"fr\">(?P<nomArticle>.*?)<\/h1>", page).group(1)

def checkFirstLinkBottom(page):
    links = re.findall("(?s)(?:<div class=\"mw-parser-output\")(?:.*?)|(<a href=\"(?P<url>/wiki/(?:.*?)?)\")|(?:<div(?! class=\"mw-parser-output\")(?:.*?)<\/div>|<div(?! class=\"mw-parser-output\")(?:.*?)<\/div>)|(?:<table class=\"infobox_v2\">(?:.*?)<\/table>)", page)
    for link in links:
        if not ':' in link:
            if link != "":
                print link
    print 'error'

def checkFirstLinkTop(page):
    links = re.findall("(?s)<div class=\"mw-parser-output\">(?:.*?)|(?:<a href=\"(?P<url>/wiki/(?:.*?)?)\")(?:.*?)<\/div>", page)
    for link in links:
        if not ':' in link:
            if link != "":
                print link
                # return link
    print 'error'

if __name__ == "__main__":
    url = "https://fr.wikipedia.org/wiki/Connaissances"
    while (1):
        page = getPage(url)
        pageName = getPageName(page)
        print pageName
        firstLink = checkFirstLinkBottom(page)
        print firstLink
        url = "https://fr.wikipedia.org" + firstLink
