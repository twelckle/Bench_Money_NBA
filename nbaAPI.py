import time

# from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
from nba_api.stats.static import teams, players
from nba_api.stats.library.parameters import SeasonType
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if different
db = client['nba_db']
salaryTeams = db['teams']
gameData = db['games']

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

def get_player_id_by_name(player_name):
    # Search for the player by full name
    search_results = players.find_players_by_full_name(player_name)
    
    if search_results:
        return search_results[0]['id']
    else:
        return None

def topPlayerCalc(playerName, money_spent, topPlayers, benchMinutes):
    for index in range(0, 3):
        if(topPlayers[index][1] < money_spent):
            playerID = get_player_id_by_name(playerName)
            insertPlayer([playerName, money_spent, playerID, benchMinutes], index, topPlayers)
            return

def addCommasNumber(number):
    integer_number = int(number)
    formatted_number = f"{integer_number:,}"
    
    return formatted_number

def returnName(name):
    firstInitial = name[0]
    spaceIndex = name.find(' ')
    if spaceIndex != -1:
        lastName = name[spaceIndex + 1:]
        return f"{firstInitial}. {lastName}"
    return name

def playerFormat(players):
    finalPlayers = []
    for player in players:
        playerName = returnName(player[0])
        str = f'{playerName}'
        finalPlayers.append(str)
    return finalPlayers

def benchMinutesFormat(players):
    benchMinutes = []
    for player in players:
        benchMin = player[3]
        benchMinutes.append(benchMin)
    return benchMinutes

def moneyFormat(players):
    finalMoney = []
    for player in players:
        str = f'${addCommasNumber(player[1])}'
        finalMoney.append(str)
    return finalMoney

def seconds_to_min_sec(seconds):
    minutes = int(seconds // 60)
    return f"({minutes} Minutes)"

def getData(year, boxscore_data, totalSeconds, money_spent, team, topPlayers):
    for index, row in boxscore_data.iterrows():
        if team != row['TEAM_ABBREVIATION']:
            if team == "":
                team = row['TEAM_ABBREVIATION']
                teamOne = team 
            else:
                team = row['TEAM_ABBREVIATION']
                teamTwo = team
                team1 = int(money_spent)
                teamOnePlayers = topPlayers.copy()
                topPlayers = [['none', 0, 0, ''], ['none', 0, 0, ''], ['none', 0, 0, '']]
            money_spent = 0
        
        playerName = row['PLAYER_NAME']
        timeAll = row['MIN']
        secondsPlayed = getTime(timeAll)

        queryPlayer = {"year": str(year), "players.name": playerName}
        projection = {"players.$": 1, "totalCapHit": 1}

        player_data = salaryTeams.find_one(queryPlayer, projection)
        if player_data is None: continue


        salary = int(player_data.get('players')[0].get('capHit')) / 82
        time_played_ratio = secondsPlayed / (totalSeconds / 5)
        bench_time = (totalSeconds / 5) - secondsPlayed
        benchMinutes = seconds_to_min_sec(bench_time)
        player_contribution = salary * time_played_ratio
        player_money_spent = (salary - player_contribution)
        money_spent += player_money_spent
        
        # print(playerName, player_money_spent, benchMinutes)
        topPlayerCalc(playerName, player_money_spent, topPlayers, benchMinutes)
    return teamOne,teamTwo,team1,money_spent,topPlayers,teamOnePlayers

def getGameInfo(game):
    game_date = game['GAME_DATE_EST']
    game_id = game['GAME_ID']
    year = getYear(game_date)
    time.sleep(1)
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    boxscore_data = boxscore.get_data_frames()[0]
    team_stats = boxscore.get_data_frames()[1]
    teamOne = boxscore_data.get('TEAM_ABBREVIATION')[0]
    teamTwo = boxscore_data.get('TEAM_ABBREVIATION')[1]
    teamOneScore = team_stats.get('PTS')[0]
    teamTwoScore = team_stats.get('PTS')[1]
    if(team_stats.get('TEAM_ABBREVIATION')[0] != teamOne):
        temp = teamOneScore
        teamOneScore = teamTwoScore
        teamTwoScore = temp
    totalSeconds = int(team_stats.get('MIN')[0][0:3]) * 60
    team1 = 0
    money_spent = 0
    team = ""
    topPlayers = [['none', 0, 0, ''], ['none', 0, 0, ''], ['none', 0, 0, '']]
    teamOnePlayers = [['none', 0, 0, ''], ['none', 0, 0, ''], ['none', 0, 0, '']]
    teamOneID = []
    teamTwoID = []
    teamOne, teamTwo, team1, money_spent, topPlayers, teamOnePlayers = getData(year, boxscore_data, totalSeconds, money_spent, team, topPlayers)

    # Finalize last team's top players
    team2 = int(money_spent)
    teamTwoPlayers = topPlayers

    for i in range(3):
        teamTwoID.append(topPlayers[i][2])
        teamOneID.append(teamOnePlayers[i][2])
    
    teamOneMoney = moneyFormat(teamOnePlayers)
    teamOneBenchMinutes = benchMinutesFormat(teamOnePlayers) 
    teamOnePlayers = playerFormat(teamOnePlayers)

    teamTwoMoney = moneyFormat(teamTwoPlayers)
    teamTwoBenchMinutes = benchMinutesFormat(teamTwoPlayers) 
    teamTwoPlayers = playerFormat(teamTwoPlayers)
    # print()
    # print(teamOnePlayers)
    # print()
    # print(teamTwoPlayers)
    # print()
    data = {
        'Team': [teamOne, teamTwo],
        'Spending': [team1, team2],
        'Players': [
            teamOnePlayers,
            teamTwoPlayers
        ],
        'Money': [
            teamOneMoney,
            teamTwoMoney
        ],
        'PlayerIDs': [
            teamOneID,
            teamTwoID
        ],
        'BenchMin': [
            teamOneBenchMinutes,
            teamTwoBenchMinutes
        ],
        'Score': [teamOneScore, teamTwoScore]
    }
    return data

# Define the date for which you want to query games

