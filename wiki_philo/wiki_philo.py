#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def checkFirstLinkBottom(page):
    # ne va chercher que dans la div mw-parser-output
    page = regex.sub("(?s).*<div class=\"mw-parser-output\">", "", page)
    # on supprime tous les tableaux (notamment le tableau a droite du texte)
    page = regex.sub("(?s)(<table(?:(?:(?:.+?(?=<table|<\/table))(?:(?!<table)|(?R))*+)*?)<\/table>)", "", page)
    # on filtre tous les liens qui ne sont ni dans des div, ni dans des parentheses, ni ce qui est entre des slashs (pour le prononciations par exemple)
    links = regex.findall("(?s)(?:<div(?:(?:(?:.+?(?=<div|<\/div))(?:(?!<div)|(?R))*+)*?)<\/div>)|(?:<a href=\"(?P<url>\/wiki\/(?:.*?)?)\")|(?:\((?:(?:(?:.+?(?=\(|\)))(?:(?!\()|(?R))*+)*?)\))|(?:\/(?=<)(?:.*?)\/(?=<))", page)
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
    nbLinks = 0
    printableList = []
    cachedEntry = []
    ended = False
    while not ended:
        nbLinks = nbLinks + 1
        page = getPage(url)
        pageName = getPageName(page)
        firstLink = checkFirstLinkBottom(page)
        printableList.append(pageName)
        cachedEntry.append(pageName)
        if firstLink != None:
            url = "https://fr.wikipedia.org" + firstLink
        else:
            ended = True
            printableList.append(" |||NOLINK|||")
            cachedEntry.append(" |||NOLINK|||")
        for entry in printableList[:-1]:
            if pageName == entry:
                ended = True
                printableList.append(" |||BOUCLE|||")
                cachedEntry.append(" |||BOUCLE|||")
        if pageName == "Philosophie":
            pageName = "{} en {} liens".format(pageName, nbLinks)
            ended = True
            printableList.append(" {} LINKS".format(nbLinks))
            cachedEntry.append(" {} LINKS".format(nbLinks))
        if not verrou._is_owned():
            with verrou:
                addEntryTableOutput(threadNumber, cachedEntry)
                printTableOutput()
                cachedEntry = []


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
        # remonte une ligne
        sys.stdout.write("\033[F")
        # efface la ligne
        sys.stdout.write("\033[K")
    sys.stdout.write(outputFinal)
    sys.stdout.flush()


def addEntryTableOutput(threadNb, cEntry):
    for entry in cEntry:
        tablePageName[threadNb - 1].append(entry)

def initTableOutput(nbThread):
    for i in xrange(nbThread):
        tablePageName.append([])
        print i + 1

def convergeToPhilo(numberOfThreads):
    initTableOutput(numberOfThreads)
    urlDepart = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    i = 0
    while i < numberOfThreads:
    # for i in range(numberOfThreads):
        if(len(threading.enumerate()) <= numberOfThreads):
            t = threading.Thread(target=randomToPhilo, args=(urlDepart, len(threading.enumerate()), ), name='EntryToPhilo')
            t.daemon = True
            t.start()
            i = i + 1

    # petite astuce pour pouvoir quitter le programme avec ctrl-c (a fix)
    i = len(threading.enumerate())
    while i > 1:
        i = len(threading.enumerate())


    # for thread in threading.enumerate():
    #     if thread.name == 'EntryToPhilo':
    #         thread.join()

verrou = threading.RLock()
tablePageName = []
rowsScreen, columnsScreen = os.popen('stty size', 'r').read().split()
columnsScreen = int(columnsScreen)

if __name__ == "__main__":
    numberOfThreads = int(sys.argv[1])
    convergeToPhilo(numberOfThreads)
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
