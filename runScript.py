from makeImage import make_image
from nbaAPI import getGameInfo
from twitter import postToTwitter
from webScrap import webScrape
from datetime import datetime, timedelta
from nba_api.stats.endpoints import scoreboardv2

def update_to_next_day(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Add one day to the date
    next_day = date_obj + timedelta(days=1)
    
    # Convert the date back to string format
    next_day_str = next_day.strftime("%Y-%m-%d")
    return next_day_str


# webScrape('2023') #This is for season 2023-2024 // Need to change to create for seasons before or after

# current_date = datetime.now().date()
current_date = '2024-4-19'
# formatted_date = current_date.strftime("%Y-%m-%d")
date = '2024-2-20'  # YYYY-MM-DD format
while(current_date != date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime("%B %d, %Y")

    # Query the NBA API for the games on the specified date
    scoreboard = scoreboardv2.ScoreboardV2(game_date=date_obj)

    # Get the game headers (details about the games)
    games = scoreboard.game_header.get_data_frame()
    for index, game in games.iterrows():
        data = getGameInfo(game)
        data['Date'] = formatted_date
        data['DateSave'] = date
        imagePath = f'{make_image(data)}.png'
        print(imagePath)
        caption = {
            'Teams': data['Team'],
            'Date': formatted_date,
            'Score': data['Score'],
        }
        postToTwitter(imagePath, caption)
        # exit()
    
    date = next_day_date = update_to_next_day(date)

