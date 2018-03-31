#!/usr/bin/python
import urllib2
import threading
import sys
import re

regexTable = '(?s)<table class="team-table table table-striped table-hover">(?:.*?)<\/table>'
regexTeams = "(?s)<tr>(.*?)<\/tr>"
# regexParserTeam = '(?s)<td>(?P<teamRank>\d*?)<\/td>(?:.*)user\?id=(?P<teamId>.*?)\">(?:.*)<span class=\"team_(?P=teamId)\">\\\\r\\\\n(?:\s*)(?P<teamName>.*?)\\\\r\\\\n(?:.*)title=\"(?P<teamCountry>.*?)\" \/>(?:.*)<td>(?P<teamScore>.*)<\/td>'
regexParserTeam = "(?s)<td>(?P<teamRank>\d*?)<\/td>(?:.*?)user\?id=(?P<teamId>\d*)(?:.*?)team_(?P=teamId)\">(?:\s*)(?P<teamname>.*?)\n(?:.*?)title=\"(?P<teamCountry>.*?)\"(?:.*?)<td>(?P<teamScore>.*?)<\/td>"
regexTeamChallenge = '(?s)<table class=\"table table-striped table-hover\"(?:.*?)<\/table>'
# regexParserChallenge = '(?s)<a href=\"(?P<challengeUrl>.*?)\">\\\\r\\\\n(?:\s*)(?P<challengeName>.*?)\\\\r\\\\n(?:.*?)<\/a>'
# regexParserChallenge = '(?s)<a href=\"(?P<challengeUrl>.*?)\">\\\\r\\\\n(?:\s*)(?P<challengeName>.*?)\\\\r\\\\n(?:\s*)<\/a>(?:.*)\((?P<challengeType>.*)\)(?:.*?)<span(?:.*?)>(?P<solvedTime>.*?)<\/span>(?:.*)<td>(?P<challengePoints>.*?)<\/td>'
regexParserChallenge = "(?s)<a href=\"(?P<challengeUrl>.*?)\">(?:\s*)(?P<challengeName>.*?)\n(?:\s*)<\/a>(?:.*)\((?P<challengeType>.*)\)(?:.*?)<span(?:.*?)>(?P<solvedTime>.*?)<\/span>(?:.*)<td>(?P<challengePoints>.*?)<\/td>"

urlRiscure = "https://rhme.riscure.com/3/"
urlScore = urlRiscure + "scores"

numberOfThreads = int(sys.argv[1])
verrou = threading.RLock()

challenges = []

def getTeamsChallenge(team):
    page = urllib2.urlopen(urlRiscure + "user?id=" + team['teamId']).read()
    solvedChallengesTable = re.search(regexTeamChallenge, page).group()
    solvedChallenges = re.findall(regexTeams, solvedChallengesTable)
    with verrou:
        for challengeTab in solvedChallenges[1:]:
            challenge = re.search(regexParserChallenge, challengeTab).groupdict()
            newChallenge = True
            for i in challenges:
                if challenge['challengeName'] == i['challengeName']:
                    newChallenge = False
                    i['solved'] = i['solved'] + 1
                    break
            if newChallenge:
                challenges.append({'challengeUrl':challenge['challengeUrl'], 'challengeType':challenge['challengeType'], 'challengeName':challenge['challengeName'], 'challengeUrl':challenge['challengeUrl'], 'solved':1, 'challengePoints':challenge['challengePoints']})

print "Get team url"
scoreBoard = urllib2.urlopen(urlRiscure + "scores").read()
teamsTable = re.search(regexTable, scoreBoard).group()
teams = re.findall(regexTeams, teamsTable)

print len(teams)
teamFilter = []
for team in teams[1:]:
    teamParsed = re.search(regexParserTeam, team).groupdict()
    teamParsed['teamScore'] = teamParsed['teamScore'].replace(',','')
    if int(teamParsed['teamScore']) > 3:
        teamFilter.append(teamParsed)

print "nb of teams : {}".format(len(teamFilter))

activeTeamCalc = 0
while activeTeamCalc < len(teamFilter):
    if(len(threading.enumerate()) <= numberOfThreads):
        t = threading.Thread(target=getTeamsChallenge, args=(teamFilter[activeTeamCalc],), name='TeamCalc')
        t.setDaemon = True;
        t.start()
        activeTeamCalc = activeTeamCalc + 1

for thread in threading.enumerate():
    if thread.name == 'TeamCalc':
        thread.join()


challengeSorted = []
challengeSorted.append(challenges[0])
for challenge in challenges[1:]:
    i = 0
    while(i != len(challengeSorted)) and (challenge['solved'] < challengeSorted[i]['solved']):
        i = i + 1
    if i == len(challengeSorted):
        challengeSorted.append(challenge)
    else:
        challengeSorted.insert(i, challenge)

print '{:<6}|{:24}|{:<24}|{:<6}|{}'.format('SOLVED','NAME','CAT','POINTS','URL')
for challenge in challengeSorted:
    print '{:<6}|{:24}|{:<24}|{:<6}|{}'.format(challenge['solved'], challenge['challengeName'], challenge['challengeType'], challenge['challengePoints'], challenge['challengeUrl'])
