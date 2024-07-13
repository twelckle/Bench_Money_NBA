import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if different
db = client['nba_db']
collection = db['teams']

class Person:
    def __init__(self, name, capHit, capPercentage):
        self.name = name
        self.capHit = capHit
        self.capPercent = capPercentage
    
    def getAll(self):
        return f"Name: {self.name}, Cap Hit: {self.capHit}, Cap Percentage: {self.capPercent}"

    def getName(self):
        return self.name

    def getCapHit(self):
       return self.capHit
    
    def getCapPercent(self):
        return self.capPercent

def removeCommas(strValue):
        value = ""
        for i in strValue:
            if i == ",":
                continue
            else:
                value = "" + value + i
        return int(value)
    
# years = ['2015','2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
years = ['2023']
teams = [
    'atlanta-hawks', 'boston-celtics', 'brooklyn-nets', 'charlotte-hornets',
    'chicago-bulls', 'cleveland-cavaliers', 'dallas-mavericks', 'denver-nuggets',
    'detroit-pistons', 'golden-state-warriors', 'houston-rockets', 'indiana-pacers',
    'la-clippers', 'los-angeles-lakers', 'memphis-grizzlies', 'miami-heat',
    'milwaukee-bucks', 'minnesota-timberwolves', 'new-orleans-pelicans', 'new-york-knicks',
    'oklahoma-city-thunder', 'orlando-magic', 'philadelphia-76ers', 'phoenix-suns',
    'portland-trail-blazers', 'sacramento-kings', 'san-antonio-spurs', 'toronto-raptors',
    'utah-jazz', 'washington-wizards'
]

count = 0
for team in teams:
    for year in years:
        nextYear = int(year)+1
        print("Year: " + year + "-" + str(nextYear) + "   " + team)
        url = f'https://www.spotrac.com/nba/{team}/cap/_/year/{year}/sort/cap_total'
        # print(url)

        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')

        table = soup.find('table', class_='table table-internal-sort rounded-top mt-2 mb-0', id='table_active')

        players = []
        totalCapHit = 0

        if (table):
            tbody = table.find('tbody')

            if(tbody):
                rows = tbody.find_all('tr')
                for row in rows:
                    data = row.find_all('td')

                    try:
                        name = data[0].find('a').text
                        capHit = data[3].find('span').text
                        percentage = data[4].find('span').text
                        name = name.strip()
                        capHit = removeCommas(capHit.strip()[1:])
                        percentage = percentage.strip()[:-1]
                        newPerson = Person(name, capHit, percentage)
                        totalCapHit += capHit

                        player_dict = {
                            "name": newPerson.getName(),
                            "capHit": newPerson.getCapHit(),
                            "capPercent": newPerson.getCapPercent()
                        }
                        players.append(player_dict)
                        # print(name, capHit, percentage)
                    except:
                        continue
                        # print("player is not important enough")
                        
                        # print(data[index].prettify())
                    # print("\nnext\n")

        team_doc = {
            "team": team,
            "year": year,
            "totalCapHit": totalCapHit,
            "players": players,
        }
        collection.insert_one(team_doc)



print("put all the data into databse")
    
