import re
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

link = "https://twitter.com/search?q=from%3Arealdonaldtrump%20since%3A2016-10-10%20until%3A2016-10-11"
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
# regex = "(<div class=\"content\"(?:.*)<\/div>)"
regexTweets = "(?s)<p class=\"TweetTextSize  js-tweet-text tweet-text\"(?:.*?)<\/p>"
regexText = "<(?:.*?)>|<(?:.*?)>"
regexEnd = "(<div class=\"timeline-end has-items \")"
# regexLink
# class="TweetTextSize  js-tweet-text tweet-text"
compiledTweets = re.compile(regexTweets)
compiledText = re.compile(regexText)
compiledEnd = re.compile(regexEnd)

# for key, value in enumerate(header):
#     capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
#     webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value
expor = 'export PATH={}:$PATH'.format(os.getcwd())

# driver = webdriver.PhantomJS(executable_path="{}/phantomjs".format(os.getcwd()))
driver = webdriver.Firefox(executable_path="{}/geckodriver".format(os.getcwd()))

# print expor
os.system(expor)

# request = requests.get(link, headers=header)

driver.get(link)
request = ""
while compiledEnd.search(request) != 'None':
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    request = driver.page_source.encode("utf-8")
    print request
# print request.text.encode('utf-8')
# print request.text.encode('utf-8')
# listString = compiledTweets.findall(request.text.encode('utf-8'))
listString = compiledTweets.findall(request)
# print listString
# print len(listString)
# if compiledEnd.search(request.text) == 'None':
#     print "ohyeah"
for i in listString:
    # print compiledText.split(str(i))
    tweet = ""
    for j in compiledText.split(str(i)):
        print j + "\n" + "_____________"
        if 'pic.twitter' in j:
            print 'mdr'
            break
        if j != '':
            print 'lol'
            tweet = tweet + j
    print repr(tweet)
    # print json.dumps({'tweet': tweet}, separators=(',',':'))
    # i = i.replace("\n", "")
    # print i + "\n"
    print "\n"
