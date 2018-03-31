#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import requests
import BeautifulSoup
import sys
import re
import datetime
import threading
import json

regexTweets = "(?s)<p class=\"TweetTextSize  js-tweet-text tweet-text\"(?:.*?)<\/p>"
regexEnd = "(<div class=\"timeline-end has-items \")"
compiledTweets = re.compile(regexTweets)
compiledEnd = re.compile(regexEnd)

def date(nbDays):
    dateDict = datetime.datetime.now() - datetime.timedelta(days=nbDays)
    return {'day': "{:0>2}".format(dateDict.day), 'month': "{:0>2}".format(dateDict.month), 'year': "{:0>4}".format(dateDict.year)}


def getTweets(link, nbDays, headers):
    dateDictLast = date(nbDays)
    dayLast = dateDictLast['day']
    monthLast = dateDictLast['month']
    yearLast = dateDictLast['year']
    # print '{}:{}:{}\n'.format(dayLast, monthLast, yearLast)
    dateDictFirst = date(nbDays - 1)
    dayFirst = dateDictFirst['day']
    monthFirst = dateDictFirst['month']
    yearFirst = dateDictFirst['year']
    # print '{}:{}:{}\n'.format(dayFirst, monthFirst, yearFirst)
    link = "https://twitter.com/search?q=from%3A{}%20since%3A{}-{}-{}%20until%3A{}-{}-{}".format(
        user, yearLast, monthLast, dayLast, yearFirst, monthFirst, dayFirst)
    # print link
    # request = urllib2.Request(link, headers=header)
    request = requests.get(link, headers=header)
    # view = urllib2.urlopen(request)
    # nice = BeautifulSoup.BeautifulSoup(view.read())
    # nice = BeautifulSoup.BeautifulSoup(request.text)
    # tweets = nice.findAll('p', {'class': "TweetTextSize  js-tweet-text tweet-text"})
    tweets = compiledTweets.findall(request.text.encode('utf-8'))
    startOk = False
    while startOk != True:
        global currentDayOrder
        if nbDays == currentDayOrder:
            currentDayOrder = currentDayOrder + 1
            startOk = True
    with verrou:
        if compiledEnd.search(request.text) == None and len(tweets) != 0:
            print link
        # if(nbDays == 99):
        #     print nice
        # print "_____________________________________________"
        # print  "{}\n".format(request.status_code)
        # print link
        # # print tweets
        # print '{}:{}:{}\n'.format(dayLast, monthLast, yearLast)
        # print 'Nombre de Tweets : {}'.format(len(tweets))
        for tweet in tweets:
            # f.write(tweet.string)
            # print tweetprint i
            global numberOfTweets
            numberOfTweets = numberOfTweets + 1
            listString = compiledRegex.split(str(tweet))
            outputString = ""
            for part in listString:
                if 'pic.twitter' in part:
                    break
                outputString = outputString + part
            # print repr(tweet)
            # with open("donald.txt", "a") as myfile:
            #    myfile.write(repr(outputString)+ "\n")
            print repr(outputString)

            print "\n-----------"


# TWITTER INFO
user = "realdonaldtrump"
link = "https://twitter.com/search?q=from%3A{}%20since%3A{}-{}-{}%20until%3A{}-{}-{}"

# OUTPUT FILE
nameOut = "donaldTweets.out"

# HEADER REQUEST
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}

# REGEX
regex = "<(?:.*?)>|<(?:.*?)>"

# THREADS
numberOfThread = int(sys.argv[1])
verrou = threading.RLock()

# TWEETS
numberOfTweets = 0

# DATE INFO
# todayDay = int(time.strftime("%d"))
# todayMon = int(time.strftime("%m"))
# todayYea = int(time.strftime("%Y"))


compiledRegex = re.compile(regex)
# with open(nameOut,'ab') as f:
i = 0
currentDayOrder = 0
while i < 3200:
    if len(threading.enumerate()) <= numberOfThread:
        t = threading.Thread(target=getTweets, args=(
            link, i, header,), name='GetTweets:{}'.format(i))
        t.daemon = True
        t.start()
        i = i + 1
        # sys.stdout.write('\r'+'{}\n'.format(3200-i))
        # sys.stdout.flush()


for thread in threading.enumerate():
    if 'GetTweets' in thread.name:
        thread.join()

# re test : <([\w]+)[^>]*>|<(.*?)>
# v2 : <(?:.*?)>|<(?:.*?)>
# v3 = (<(?:.*?)>|<(?:.*?)>)

print "Nombre de Tweets : {}".format(numberOfTweets)
