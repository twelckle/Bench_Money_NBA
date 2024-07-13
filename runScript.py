from makeImage import make_image
from nbaAPI import getGameInfo
from datetime import datetime
from nba_api.stats.endpoints import scoreboardv2

date = '2024-04-10'  # YYYY-MM-DD format
date_obj = datetime.strptime(date, '%Y-%m-%d')

# Query the NBA API for the games on the specified date
scoreboard = scoreboardv2.ScoreboardV2(game_date=date_obj)

# Get the game headers (details about the games)
games = scoreboard.game_header.get_data_frame()
for index, game in games.iterrows():
    data = getGameInfo(game)
    data['Date'] = date
    make_image(data)

