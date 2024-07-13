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


teamIDs = [ 
    1610612737, 1610612738, 1610612739, 1610612740, 1610612741, 1610612742, 
    1610612743, 1610612744, 1610612745, 1610612746, 1610612747, 1610612748, 
    1610612749, 1610612750, 1610612751, 1610612752, 1610612753, 1610612754, 
    1610612755, 1610612756, 1610612757, 1610612758, 1610612759, 1610612760, 
    1610612761, 1610612762, 1610612763, 1610612764, 1610612765, 1610612766,
]

seasons = ['2023-24']

# teamIDs = [1610612744]

totalGames = 0
lessMoneyOnBenchWins = 0
teamWins = 0



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

def getGameInfo(games, teamID):
    
    for index, row in games.iterrows():
        game_date = row['GAME_DATE']
        game_id = row['GAME_ID']
        year = getYear(game_date)
        # print(f"Getting boxscore for game ID: {game_id} on day {game_date}")
        # Get the boxscore
        time.sleep(1)
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        boxscore_data = boxscore.get_data_frames()[0]  # You can also get other data frames depending on what you need
        team_stats = boxscore.get_data_frames()[1]

        teamOneID = str(team_stats.get('TEAM_ID'))
        teamOneWins = 0
        teamScores = team_stats.get('PTS')
        if(int(teamScores[0]) > int(teamScores[1])):
            teamOneWins = 1
        team1 = 0
        money_spent = 0
        team = ""
        teamOneCapHit = 0
        teamTwoCapHit = 0
        money_per_point = 0
        for index, row in boxscore_data.iterrows():
            if(team != row['TEAM_ABBREVIATION']):
                if(team == ""):
                    team = row['TEAM_ABBREVIATION']
                else:
                    team = row['TEAM_ABBREVIATION']
                    team1 = money_spent
                money_spent = 0
            playerName = row['PLAYER_NAME']
            playerPoints = row['PTS']

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

            timeAll = row['MIN']
            seconds = getTime(timeAll)
            totalSeconds = int(team_stats.get('MIN')[0][0:3])*60
            time_played_ratio = seconds / (totalSeconds/5)
            salary_per_game = int(player_data.get('players')[0].get('capHit')) / 82
            player_contribution = salary_per_game * time_played_ratio
            money_spent_for_player_on_bench = salary_per_game - player_contribution
            money_spent += money_spent_for_player_on_bench
            print(playerName, money_spent_for_player_on_bench, "|", salary_per_game)
            if(playerPoints != None and playerPoints != 0):
                money_per_point = playerPoints/salary_per_game
            # print(playerName + " = " + str(salary - player_contribution))

        team2 = money_spent

        winningTeam = 'team1' if teamOneWins else 'team2'
        print(f"team1 {team1}  team2 {team2} winner: {winningTeam}")
        # print(f"Team1 Cap hit: {teamOneCapHit}  team2 cap hit: {teamTwoCapHit}")

        # if(team1 < team2 and teamOneWins):
        #     lessMoneyOnBenchWins += 1
        # elif(team2 < team1 and not teamOneWins):
        #     lessMoneyOnBenchWins += 1
        
        # if(teamOneID == teamID and team1 < team2):
        #     teamWins += 1
        # elif(teamOneID != teamID and team1 > team2):
        #     teamWins += 1

        # totalGames += 1


        # Print the boxscore (or you can store it in a list, save to a file, etc.)
        # print(boxscore_data)

for season in seasons:
    for team_id in teamIDs:
        teamName = str(teams.find_team_name_by_id(team_id)['full_name'])
        print("" + str(season) + " " + teamName)
        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season, season_type_nullable=SeasonType.regular)
        games = gamefinder.get_data_frames()[0]
        getGameInfo(games, team_id)
        # print(games)
        print()
        print("total games: " + str(totalGames))
        print(f"team with less money on bench won {lessMoneyOnBenchWins} times")
        print("percentage: "+ str(lessMoneyOnBenchWins/totalGames))
        print(f"{teamName} won: {teamWins}")
# # print(lookAt_game_Date.head())

