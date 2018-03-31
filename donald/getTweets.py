# -*- coding: utf-8 -*-

import urllib2
import BeautifulSoup
import requests

link = 'https://twitter.com/search?q=from%3Arealdonaldtrump%20since%3A2017-11-11%20until%3A2017-11-23&src=typd&lang=fr'
link = 'https://twitter.com/search?q=from%3Arealdonaldtrump%20since%3A2017-11-28%20until%3A2017-11-29'
# view = urllib2.urlopen(link).read()
# payload = {'_twitter_sess,': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%0ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCN6sPghgAToMY3NyZl9p%0AZCIlNWNmNjQxOWIxMzNhMGQzN2RlYmYzZWM1YjFiOWExZDU6B2lkIiU2N2E5%0ANzI2NjFlZDUxOGRhMzhiNjc0MjA2MDdjNzcyYg%3D%3D--09c1d6bcc48fdce9272aadd1886c219f9321ed24',
#            'personalization_id':	'"v1_1Dc5inWwWeWBqbdHBhwWNQ=="',
#            'lang': 'fr',
#            'guest_id	v1': '151196681340140869',
#            'ct0': '5fa37d942598f197bd4f62a38744917b',
#            '_ga': 'GA1.2.753723709.1511966816',
#            '_gid':	'GA1.2.99688899.1511966816',
#            'eu_cn':	'1',
#            'gt':	'935882806227501057',
#            '_gat':	'1'}
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
# view = requests.get(link, headers=header).text
request = urllib2.Request(link, headers=header)
view = urllib2.urlopen(request)
nice = BeautifulSoup.BeautifulSoup(view)
tweets = nice.findAll('p', {'class': "TweetTextSize  js-tweet-text tweet-text"})
# print nice
print len(tweets)
