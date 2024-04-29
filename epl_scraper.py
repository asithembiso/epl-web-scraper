from lxml import html
import requests
from bs4 import BeautifulSoup
import re

page = requests.get('https://www.premierleague.com/clubs')
tree = html.fromstring(page.content)

linkLocation = tree.cssselect('.club-card')
teamLinks = []

for x in range(0, 20):
    # ...Find the page the link is going to...
    temp = linkLocation[x].attrib['href']

    # ...Add the link to the website domain...
    temp = "https://www.premierleague.com/" + temp

    # ...Change the link text so that it points to the squad list, not the page overview...
    temp = temp.replace("overview", "squad")

    # ...Add the finished link to our teamLinks list...
    teamLinks.append(temp)

playerLink1 = []
playerLink2 = []

# For each team link page...
for y in range(len(teamLinks)):

    # ...Download the team page and process the html code...
    squadPage = requests.get(teamLinks[y])
    squadTree = html.fromstring(squadPage.content)

    playerLocation = squadTree.cssselect('.stats-card__wrapper')

    # ...For each player link within the team page...
    for z in range(len(playerLocation)):
        # ...Save the link, complete with domain...
        playerLink1.append("https://www.premierleague.com/" + playerLocation[z].attrib['href'])

        # ...For the second link, change the page from player overview to stats
        playerLink2.append(playerLink1[z].replace("overview", "stats"))
        break
    break

print(playerLink2)
url = playerLink2[0]

req = requests.get(url).text
soup = BeautifulSoup(req, 'lxml')

# Find all player elements (assuming they have the class 'row player-10-')
players = soup.find_all('ul', attrs={'class': re.compile('player-stats__stats-wrapper')})

for player in players:
    stats = player.find_all('span', {'class': 'allStatContainer'})
    for stat in stats:
        data_stat = stat['data-stat']
        value = stat.get_text().strip()
        print(f"Data-stat: {data_stat}, Value: {value}")
    break

#print(players)
