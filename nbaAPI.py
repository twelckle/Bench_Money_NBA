import time

# from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
from nba_api.stats.static import teams
from nba_api.stats.library.parameters import SeasonType
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if different
db = client['nba_db']
salaryTeams = db['teams']
gameData = db['games']

'''
Check to see if that ID is already in the database
If yes
    -> add to the entry team x and the calculations
If no
    -> create entry and add team y and the calculations
Entry includes
    -gameID ('GameID')
    -matchup ('MATCHUP')
    -location ()
    -game date ('GAME_DATE')
    -season_id ('SEASON_ID')

'''



# nba_teams = teams.get_teams()
# # Select the dictionary for the Celtics, which contains their team ID
# minnesota = [team for team in nba_teams if team['abbreviation'] == 'MIN'][0]
# minnesota_id = minnesota['id']

# gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=minnesota_id)
# # The first DataFrame of those returned is what we want.
# games = gamefinder.get_data_frames()[0]
# games.head()

# gameDate = '2018-04-04'
# lookAt_game_Date = games.sort_values(gameDate).iloc[-1]

# seasons = [
#     '2023-24', '2022-23', '2021-22', '2020-21', '2019-20', '2018-19', 
#     '2017-18', '2016-17', '2015-16'
# ]



# team_id = 1610612744

# # Define the season (example for the 2023-24 season)
# season = '2023-24'

# # Step 1: Get the list of games for the team this season

# team_id = 1610612744

# # Define the season
# season = '2023-24'

# # Step 1: Get the list of games for the team this season
# gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season)

# # Print the JSON response
# print(gamefinder.get_dict())

def getYear(dateStr):
    year = int(dateStr[0:4])
    month = dateStr[5:7]
    if(int(month) < 9):
        year -= 1
    return year

def getTime(timeAll):
    if(timeAll == None):
        return 0
    
    timeAll = str(timeAll)
    minutes = timeAll[:2]
    if(minutes[-1:] == '.'):
        minutes = minutes[0:1]
    seconds = int(timeAll[-2:])
    seconds += int(minutes)*60
    return seconds

def insertPlayer(data, index, array):
    if(index > 2): return
    temp = array[index]
    array[index] = data
    data = temp
    insertPlayer(data, index+1, array)

def makePlayerNameSmaller(name):
    # if(name == 'Shai Gilgeous-Alexander'):
    #     return 'SGA'
    if(len(name) <= 18):
        return name
    else:
        return name[0:18]

def topPlayerCalc(playerName, money_spent, topPlayers):
    for index in range(0, 3):
        if(topPlayers[index][1] < money_spent):
            playerName = makePlayerNameSmaller(playerName)
            insertPlayer([playerName, money_spent], index, topPlayers)
            return

def addCommasNumber(number):
    integer_number = int(number)
    formatted_number = f"{integer_number:,}"
    
    return formatted_number

def playerFormat(players):
    finalPlayers = []
    for player in players:
        str = f'• {player[0]}: ${addCommasNumber(player[1])}'
        finalPlayers.append(str)
    return finalPlayers


def getGameInfo(game):
    game_date = game['GAME_DATE_EST']
    game_id = game['GAME_ID']
    year = getYear(game_date)
    # print(f"Getting boxscore for game ID: {game_id} on day {game_date}")
    # Get the boxscore
    time.sleep(1)
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    boxscore_data = boxscore.get_data_frames()[0]  # You can also get other data frames depending on what you need
    team_stats = boxscore.get_data_frames()[1]
    teamOne = team_stats.get('TEAM_ABBREVIATION')[0]
    teamTwo = team_stats.get('TEAM_ABBREVIATION')[1]

    winningTeam = teamTwo
    totalSeconds = int(team_stats.get('MIN')[0][0:3])*60
    teamScores = team_stats.get('PTS')
    if(int(teamScores[0]) > int(teamScores[1])):
        winningTeam = teamOne
    team1 = 0
    money_spent = 0
    team = ""
    topPlayers = [['none', 0], ['none', 0], ['none', 0]]
    teamOneCapHit = 0
    teamTwoCapHit = 0
    for index, row in boxscore_data.iterrows():
        if(team != row['TEAM_ABBREVIATION']):
            if(team == ""):
                team = row['TEAM_ABBREVIATION']
            else:
                team = row['TEAM_ABBREVIATION']
                team1 = int(money_spent)
                teamOnePlayers = topPlayers
                topPlayers = topPlayers = [['none', 0], ['none', 0], ['none', 0]]
            money_spent = 0
        playerName = row['PLAYER_NAME']
        timeAll = row['MIN']
        secondsPlayed = getTime(timeAll)

        # Query to find the player in the 'players' array
        queryPlayer = {"year": str(year) ,"players.name": playerName}

        # Projection to include only the players array
        projection = {"players.$": 1, "totalCapHit": 1}

        player_data = salaryTeams.find_one(queryPlayer, projection)
        if(player_data == None): continue

        if(teamOneCapHit != 0 and int(player_data.get('totalCapHit')) != teamOneCapHit):
            teamTwoCapHit = int(player_data.get('totalCapHit'))
        elif(teamOneCapHit == 0):
            teamOneCapHit = int(player_data.get('totalCapHit'))

        # salary_ratio = int(player_data.get('players')[0].get('capHit')) / int(player_data.get('totalCapHit'))
        # time_played_ratio = seconds / (totalSeconds/5)
        # player_contribution = salary_ratio * time_played_ratio
        # money_spent += player_contribution

        salary = int(player_data.get('players')[0].get('capHit')) / 82
        time_played_ratio = secondsPlayed / (totalSeconds/5)
        player_contribution = salary * time_played_ratio
        player_money_spent = (salary-player_contribution)
        money_spent += player_money_spent
        print(playerName, player_money_spent)
        # print(playerName + " = " + str(salary - player_contribution))
        topPlayerCalc(playerName, player_money_spent, topPlayers)

    team2 = int(money_spent)
    teamTwoPlayers = playerFormat(topPlayers)
        # team1 = team1 / (teamOneCapHit/82)
        # team2 = team2 / (teamTwoCapHit/82)

    teamOnePlayers = playerFormat(teamOnePlayers)
    data = {
        'Team': [teamOne, teamTwo],
        'Spending': [team1, team2],
        'Players': [
            teamOnePlayers,
            teamTwoPlayers
        ],
        'WinningTeam': winningTeam,
        'Score': [int(teamScores[0]), int(teamScores[1])]
    }

    return data

# Define the date for which you want to query games

