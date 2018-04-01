import urllib2
import regex
import sys
import os
import threading

# (?s)<div(?:(?:[^(<]*+(?:(?!<div)|(?0))*+)*+)<\/div>

# (<div(?:(?:(.+?(?=<div|<\/div))((?!<div)|(?1))*+)*?)<\/div>)

# interessant :(?s)<div class=\"mw-parser-output\"(?:.*?)|(?:<a href=\"(?P<url>\/wiki\/(?:.*?)?)\")|(?:<div(?:(?:(?:.+?(?=<div|<\/div))(?:(?!<div)|(?0))*+)*?)<\/div>)

def getPage(url):
    return urllib2.urlopen(url).read()

def getPageName(page):
    name = regex.search("<h1 id=\"firstHeading\" class=\"firstHeading\" lang=\"fr\">(?P<nomArticle>.*?)<\/h1>", page).group(1)
    name = regex.sub("<(.*?)>", "", name)
    return name

# def checkFirstLinkBottom(page):
#     links = re.findall("(?s)<div class=\"mw-parser-output\"(?:.*?)|(?:<a href=\"(?P<url>/wiki/(?:.*?)?)\")|(?:<div(?:.*?)<\/div>|<div(?:.*?)<\/div>)|(?:<table class=\"infobox_v2\">(?:.*?)<\/table>)", page)
#     for link in links:
#         if not ':' in link:
#             if link != "":
#                 return link
#     print 'error'

def checkFirstLinkBottom(page):
    page = regex.sub("(?s).*<div class=\"mw-parser-output\">", "", page)
    links = regex.findall("(?s)(?:<div(?:(?:(?:.+?(?=<div|<\/div))(?:(?!<div)|(?R))*+)*?)<\/div>)|(?:<table class=\"infobox_v2\"(?:.*?)<\/table>)|(?:<a href=\"(?P<url>\/wiki\/(?:.*?)?)\")", page)
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

def randomToPhilo(url, threadNumber):
    pageName = ""
    printableList = ""
    while pageName != "Philosophie":
        page = getPage(url)
        pageName = getPageName(page)
        printableList = printableList + "->" + pageName
        firstLink = checkFirstLinkBottom(page)
        url = "https://fr.wikipedia.org" + firstLink
        with verrou:
            addEntryTableOutput(threadNumber, pageName)
            printTableOutput()


def printTableOutput():
    outputFinal = ""
    outputLine = ""
    for i in range(len(tablePageName)):
        outputLine = " {} :".format(i + 1)
        for entry in tablePageName[i]:
            outputLine = outputLine + "->" + entry
        if len(outputLine) > columnsScreen:
            outputLine = outputLine[(len(outputLine)- columnsScreen):]
        outputFinal = outputFinal + outputLine + "\n"
        outputLine = ""
    for i in range(len(tablePageName)):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
    sys.stdout.write(outputFinal)
    sys.stdout.flush()


def addEntryTableOutput(threadNb, entry):
    tablePageName[threadNb - 1].append(entry)

def initTableOutput(nbThread):
    for i in xrange(nbThread):
        tablePageName.append([])
        print i + 1

def convergeToPhilo(numberOfThreads):
    initTableOutput(numberOfThreads)
    urlDepart = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    for i in range(numberOfThreads):
        if(len(threading.enumerate()) <= numberOfThreads):
            t = threading.Thread(target=randomToPhilo, args=(urlDepart, len(threading.enumerate()), ), name='EntryToPhilo')
            t.setDaemon = True;
            t.start()

    for thread in threading.enumerate():
        if thread.name == 'EntryToPhilo':
            thread.join()

verrou = threading.RLock()
tablePageName = []
rowsScreen, columnsScreen = os.popen('stty size', 'r').read().split()
columnsScreen = int(columnsScreen)

if __name__ == "__main__":
    numberOfThreads = int(sys.argv[1])
    convergeToPhilo(numberOfThreads)
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    #
    # while (1):
    #     page = getPage(url)
    #     pageName = getPageName(page)
    #     print pageName
    #     firstLink = checkFirstLinkBottom(page)
    #     print firstLink
    #     url = "https://fr.wikipedia.org" + firstLink
