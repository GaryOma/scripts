import urllib2
import regex
import sys
import threading

# (?s)<div(?:(?:[^(<]*+(?:(?!<div)|(?0))*+)*+)<\/div>

# (<div(?:(?:(.+?(?=<div|<\/div))((?!<div)|(?1))*+)*?)<\/div>)

# interessant :(?s)<div class=\"mw-parser-output\"(?:.*?)|(?:<a href=\"(?P<url>\/wiki\/(?:.*?)?)\")|(?:<div(?:(?:(?:.+?(?=<div|<\/div))(?:(?!<div)|(?0))*+)*?)<\/div>)

def getPage(url):
    return urllib2.urlopen(url).read()

def getPageName(page):
    return regex.search("<h1 id=\"firstHeading\" class=\"firstHeading\" lang=\"fr\">(?P<nomArticle>.*?)<\/h1>", page).group(1)

# def checkFirstLinkBottom(page):
#     links = re.findall("(?s)<div class=\"mw-parser-output\"(?:.*?)|(?:<a href=\"(?P<url>/wiki/(?:.*?)?)\")|(?:<div(?:.*?)<\/div>|<div(?:.*?)<\/div>)|(?:<table class=\"infobox_v2\">(?:.*?)<\/table>)", page)
#     for link in links:
#         if not ':' in link:
#             if link != "":
#                 return link
#     print 'error'

def checkFirstLinkBottom(page):
    page = regex.sub("(?s).*<div class=\"mw-parser-output\">", "", page)
    links = regex.findall("(?s)(?:<div(?:(?:(?:.+?(?=<div|<\/div))(?:(?!<div)|(?R))*+)*?)<\/div>)|(?:<a href=\"(?P<url>\/wiki\/(?:.*?)?)\")", page)
    # print links
    for link in links:
        if not ':' in link:
            if link != "":
                return link


def checkFirstLinkTop(page):
    links = re.findall("(?s)<div class=\"mw-parser-output\">(?:.*?)|(?:<a href=\"(?P<url>/wiki/(?:.*?)?)\")(?:.*?)<\/div>", page)

    for link in links:
        if not ':' in link:
            if link != "":
                print link
                # return link
    print 'error'

if __name__ == "__main__":
    numberOfThreads = int(sys.argv[1])
    verrou = threading.RLock()
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    while (1):
        page = getPage(url)
        pageName = getPageName(page)
        print pageName
        firstLink = checkFirstLinkBottom(page)
        print firstLink
        url = "https://fr.wikipedia.org" + firstLink
